import praw
import json
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
import static_backtick
import re
from typing import TextIO
import prawcore.exceptions

logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)s %(message)s')

def is_opt_out_attempt(comment: str, author: str, opt_out_accounts: list):
    return (comment == static_backtick.opt_out_string and author not in opt_out_accounts)

def opt_out_user(username: str, opt_out_accounts: list, opt_out_file: TextIO):
    # some pass-by-reference magic
    opt_out_accounts.append(username)
    json.dump(opt_out_accounts, opt_out_file)

def backtick_codeblock_used(regex: str, comment: str):
    match = re.search(regex, comment, re.M)
    return bool(match)

def is_already_responded(comment: str, responded_comments: list):
    return (comment in responded_comments)

def is_opted_out(author: str, opt_out_accounts: list):
    return (author in opt_out_accounts)

def add_to_responded_comments(comment: str, responded_comments: list, responded_comments_file: TextIO):
    responded_comments.append(comment)
    json.dump(responded_comments, responded_comments_file)

def is_subreddit_blacklisted(subreddit: str, blacklist: list):
    return (subreddit in blacklist)

if __name__ == "__main__":
    env_path = Path('.') / 'secrets' / '.env'
    load_dotenv(dotenv_path=env_path)

    logger = logging.getLogger("backtickbot")
    logger.info("startng...")

    with open(static_backtick.responded_comments_file, 'r') as f:
        responded_comments = json.load(f)

    with open(static_backtick.opt_out_file, 'r') as f:
        opt_out_accounts = json.load(f)

    reddit = praw.Reddit(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"]
    )

    subreddit = reddit.subreddit(os.environ["SUBREDDIT"])

    for comment in subreddit.stream.comments():
        if is_subreddit_blacklisted(comment.subreddit.display_name.lower(), static_backtick.sub_blacklist):
            continue

        # incase of restarts this might accidently happen
        if is_already_responded(comment.id, responded_comments):
            logger.info(f"skipping, already responded to comment {comment.id}")
            continue

        if is_opted_out(comment.author.name, opt_out_accounts):
            logger.info(f"skipping opted out user {comment.author.name}")
            continue

        if is_opt_out_attempt(comment.body, comment.author.name, opt_out_accounts):
            logger.info(f"opting out user {comment.author.name}")
            with open(static_backtick.opt_out_file, 'w+') as f:
                opt_out_user(comment.author.name, opt_out_accounts, f)
            
            comment.author.message("Opt out confirmation.", static_backtick.opt_out_confirmation_message.format(username=comment.author.name))
            logger.info(f"sent confirmation message to {comment.author.name}")

        if backtick_codeblock_used(static_backtick.detection_regex, comment.body):
            logger.info(f"detected match {comment.id}, attempting response")

            with open(static_backtick.responded_comments_file, 'w+') as f:
                add_to_responded_comments(comment.id, responded_comments, f)

            try:
                comment.reply(static_backtick.response.format(username=comment.author.name))
            except prawcore.exceptions.Forbidden as e:
                logger.exception(f"banned from subreddit {comment.subreddit.display_name}, {e}")