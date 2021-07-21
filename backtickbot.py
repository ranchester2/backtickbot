import praw
import json
from dotenv import load_dotenv
from pathlib import Path
import os
import shutil
import sys
import logging
import static_backtick
import re
from typing import TextIO
import prawcore.exceptions
import praw.models


def escape_username(username: str) -> str:
    """
    Convert the username into escaping all special
    reddit markdown charachters for correct tagging
    in message
    """
    fixed = ""

    for char in username:
        if char in ["_", "*", "`", "#"]:
            # Double backslash because we are fixing reddit's formatting
            # not outs
            fixed += ("\\" + char)
        else:
            fixed += char

    return fixed


def gen_old_webpage(comment_html: str, comment_id):
    """
    Generates an html file of how the comment
    would look like on old reddit
    """
    with open("data/comment_template.html", "r") as f:
        template = f.read()
    template = template.replace("<body></body>", f"<body>{comment_html}</body>")
    with open(Path(os.environ["SERVER_STORAGE_LOCATION"]) / (comment_id + ".html"), "w") as f:
        f.write(template)


def capture_preview(preview_url: str, comment_id: str):
    os.system(
        f"firefox-esr --screenshot {os.environ['SERVER_STORAGE_LOCATION']}/{comment_id}.png {preview_url} && chmod 755 {os.environ['SERVER_STORAGE_LOCATION']}/{comment_id}.png"
    )


def convert_text_to_correct_codeblocks(regex: str, text: str) -> str:
    """
    Converts text to the correct formatting so that we can let users read it
    """
    incorrect_codeblocks = re.findall(regex, text, re.M)

    correct_codeblocks = []

    for codeblock in incorrect_codeblocks:
        # Taken from stackoverflow, removes the first and last line because they are only backtick
        codeblock = codeblock.split("\n", 1)[1]
        codeblock = "\n".join(codeblock.split("\n")[:-1])

        # For it to render properly on reddit, there needs to be a line before and possibly after

        codeblock = re.sub(r'^', '    ', codeblock, flags=re.M)
        codeblock = "\n" + codeblock + "\n"

        correct_codeblocks.append(codeblock)

    for index, incorrect_codeblock in enumerate(incorrect_codeblocks):
        text = text.replace(incorrect_codeblock, correct_codeblocks[index])

    return text


def is_opt_out_attempt(comment: str, author: str, opt_out_accounts: list) -> bool:
    return (comment == static_backtick.opt_out_string and author not in opt_out_accounts)


def is_dmmode_opt_attempt(comment: str, author: str, dmmode_accounts: list) -> bool:
    return (comment == static_backtick.dmmode_string and author not in dmmode_accounts)


def dmmode_opt_user(username: str, dmmode_accounts: list, dmmode_file: TextIO):
    dmmode_accounts.append(username)
    json.dump(dmmode_accounts, dmmode_file)


def opt_out_user(username: str, opt_out_accounts: list, opt_out_file: TextIO):
    # some pass-by-reference magic
    opt_out_accounts.append(username)
    json.dump(opt_out_accounts, opt_out_file)


def backtick_codeblock_used(regex: str, comment: str) -> bool:
    match = re.search(regex, comment, flags=re.M)
    return bool(match)


def is_already_responded(comment: str, responded_comments: list) -> bool:
    return (comment in responded_comments)


def is_opted_out(author: str, opt_out_accounts: list) -> bool:
    return (author in opt_out_accounts)


def is_in_dmmode(author: str, dmmode_accounts: list) -> bool:
    return (author in dmmode_accounts)


def add_to_responded_comments(comment: str, responded_comments: list, responded_comments_file: TextIO):
    responded_comments.append(comment)
    json.dump(responded_comments, responded_comments_file)


def is_subreddit_blacklisted(subreddit: str, blacklist: list) -> bool:
    return (subreddit in blacklist)


def is_restart_request(comment: str, restart_key: str) -> bool:
    return (comment == restart_key)


def main(subreddit: praw.models.Subreddit, reddit: praw.Reddit, logger, responded_comments: list, opt_out_accounts: list, dmmode_accounts: list):
    for comment in subreddit.stream.comments():
        if is_subreddit_blacklisted(comment.subreddit.display_name.lower(), static_backtick.sub_blacklist):
            continue

        # incase of restarts this might accidently happen
        if is_already_responded(comment.id, responded_comments):
            logger.info(f"skipping, already responded to comment {comment.id}")
            continue

        if is_restart_request(comment.body, os.environ["RESTART_KEY"]):
            logger.info(
                f"received restart request in comment {comment.id}, restarting...")
            exit(0)

        if is_opted_out(comment.author.name, opt_out_accounts):
            logger.info(f"skipping opted out user {comment.author.name}")
            continue

        if is_opt_out_attempt(comment.body, comment.author.name, opt_out_accounts):
            logger.info(f"opting out user {comment.author.name}")
            with open(static_backtick.opt_out_file, 'w+') as f:
                opt_out_user(comment.author.name, opt_out_accounts, f)

            comment.author.message(
                "Opt out confirmation.",
                static_backtick.opt_out_confirmation_message.format(
                    username=comment.author.name
                )
            )
            logger.info(
                f"sent opt-out confirmation message to {comment.author.name}")

        if is_dmmode_opt_attempt(comment.body, comment.author.name, dmmode_accounts):
            logger.info(f"changing user {comment.author.name} to dmmode")
            with open(static_backtick.dmmode_file, 'w+') as f:
                dmmode_opt_user(comment.author.name, dmmode_accounts, f)

            comment.author.message(
                "DMMode confirmation.",
                static_backtick.dmmode_confirmation_message.format(
                    username=comment.author.name
                )
            )

        if backtick_codeblock_used(static_backtick.detection_regex, comment.body):
            logger.info(f"detected match {comment.id}, attempting response")

            with open(static_backtick.responded_comments_file, 'w+') as f:
                add_to_responded_comments(comment.id, responded_comments, f)

            try:
                gen_old_webpage(comment.body_html, comment.id)
                logger.info("succesfully generated and saved old reddit preview")

                # The post is what we will link to users so that they will know how the comment is
                converted = reddit.subreddit(os.environ["CONVERSIONS_SUBREDDIT"]).submit(
                    title=f"https://np.reddit.com{comment.permalink}",
                    selftext=convert_text_to_correct_codeblocks(
                        static_backtick.detection_regex,
                        comment.body
                    )
                )
                logger.info("succesfully posted conversion")

                capture_preview(f"{os.environ['PREVIEW_STORAGE_URL']}{comment.id}{'.html'}", comment.id)
                logger.info("succesfully captured incorrect preview")

                if is_in_dmmode(comment.author.name, dmmode_accounts):
                    comment.author.message(
                        "Backtick format allert",
                        static_backtick.response.format(
                            username=escape_username(comment.author.name),
                            fixed_url=f"https://np.reddit.com{converted.permalink}",
                            incorrect_screenshot=f"{os.environ['PREVIEW_STORAGE_URL']}{comment.id}{'.png'}",
                            incorrect_link=f"{os.environ['PREVIEW_STORAGE_URL']}{comment.id}{'.html'}",
                            codeblock_url=static_backtick.new_reddit_codeblock_url,
                            opt_out_message=static_backtick.opt_out_string
                        )
                    )
                else:
                    comment.reply(
                        static_backtick.response.format(
                            username=escape_username(comment.author.name),
                            fixed_url=f"https://np.reddit.com{converted.permalink}",
                            incorrect_screenshot=f"{os.environ['PREVIEW_STORAGE_URL']}{comment.id}{'.png'}",
                            incorrect_link=f"{os.environ['PREVIEW_STORAGE_URL']}{comment.id}{'.html'}",
                            codeblock_url=static_backtick.new_reddit_codeblock_url,
                            opt_out_message=static_backtick.opt_out_string
                        )
                    )
                logger.info("succesfully posted response")
            except prawcore.exceptions.Forbidden as e:
                logger.exception(
                    f"banned from subreddit {comment.subreddit.display_name}, {e}")


if __name__ == "__main__":
    env_path = Path('.') / 'secrets' / '.env'
    load_dotenv(dotenv_path=env_path)

    shutil.copy2("data/comment_template.css", os.environ["SERVER_STORAGE_LOCATION"])
    shutil.copy2("data/coment_template.html", os.environ["SERVER_STORAGE_LOCATION"])

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        handlers=[
            logging.FileHandler(os.environ["LOG_FILE"]),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger("backtickbot")
    logger.info("startng...")

    with open(static_backtick.responded_comments_file, 'r') as f:
        responded_comments = json.load(f)

    with open(static_backtick.opt_out_file, 'r') as f:
        opt_out_accounts = json.load(f)

    with open(static_backtick.dmmode_file, 'r') as f:
        dmmode_accounts = json.load(f)

    reddit = praw.Reddit(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"]
    )

    reddit.validate_on_submit = True

    subreddit = reddit.subreddit(os.environ["SUBREDDIT"])

    main(subreddit, reddit, logger, responded_comments,
         opt_out_accounts, dmmode_accounts)
