import praw
import json
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
import static_backtick
import re

logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)s %(message)s')

def handle_backticks(reddit: praw.Reddit, subreddit: praw.models.Subreddit, responded_comments: list, optout_accounts: list):
    logger = logging.getLogger("backtickbot")
    for comment in subreddit.stream.comments():
        # Step one is test wether it is from a blacklisted subreddit
        if comment.subreddit.display_name.lower() in static_backtick.disallowed:
            #logger.info(f"skipping comment from subreddit {comment.subreddit.display_name.lower()}")
            continue

        # Have we already responded to the comment?
        if comment.id in responded_comments:
            logger.info(f"skipping already responded to comment {comment.id}")
            continue

        # Has the user opted out?
        if comment.author.name in optout_accounts:
            logger.info(f"skipping opted out user {comment.author.name}")
            continue

        # check if a comment is an opt out attempt
        if comment.body == "backtickopt6":
            if comment.author.name not in optout_accounts:
                optout_accounts.append(comment.author.name)
                logger.info(f"opting out user {comment.author.name}")
                with open("runtime/optout.json", "w+") as f:
                    json.dump(optout_accounts, f)
                
                comment.author.message("Opt out confirmation", static_backtick.opt_out.format(username=comment.author.name))
                logger.info(f"sent confirmation message to {comment.author.name}")


        # Does it match the regex?
        match = re.search("^`{3}[^\n`]{0,7}\n[^`]*^`{3}", comment.body)
        if match:
            logger.info(f"detected match {comment.id}, attempting response")
            responded_comments.append(comment.id)
            with open("runtime/responses.json", 'w+') as f:
                json.dump(responded_comments, f)
            
            try:
                comment.reply(static_backtick.response.format(username=comment.author.name))
            except Exception as e:
                logger.exception(f"cannot reply {e}")
    



if __name__ == "__main__":
    logger = logging.getLogger("backtickbot")
    logger.info("startng...")

    with open("runtime/responses.json", 'r') as f:
        responded_comments = json.load(f)

    with open("runtime/optout.json", 'r') as f:
        optout_accounts = json.load(f)

    env_path = Path('.') / 'secrets' / '.env'
    load_dotenv(dotenv_path=env_path)

    reddit = praw.Reddit(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"]
    )

    subreddit = reddit.subreddit("all")

    handle_backticks(reddit, subreddit, responded_comments, optout_accounts)
