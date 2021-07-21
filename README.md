# Backtickbot
A crappy bot that informs about backtick codeblock syntax

### Inspiration
Saw that a subreddit had a automoderator informing of this.
### How to run?

Create a folder called `runtime`
and in it put:

* `dmmode.json` - content should be `[]`
* `responses.json` - content should be `[]`
* `optout.json` - content should be `[]`

Install requirements.txt and run backtickbot.py

There is also a terrible dockerfile setup, so you can use that.
But make sure to have a config volume to `/app/secrets`, a data volume
at `/app/runtime` and bind mount the webserver directory to `/app/webdata`

You also need a .env file in secrets/.env

```sh
CLIENT_ID=<your client id>
CLIENT_SECRET=<your client secret>
REDDIT_USER_AGENT=<your useragent>
REDDIT_USERNAME=<your reddit username>
REDDIT_PASSWORD=<your reddit passwd>
SUBREDDIT=<what subreddit will it run on>
CONVERSIONS_SUBREDDIT=<to what subreddit will the conversion posts be posted on>
RESTART_KEY=<string used to restart the bot remotely>
LOG_FILE=<where the log file will be>
SERVER_STORAGE_LOCATION=<writable storage that shows up in url>
PREVIEW_STORAGE_URL=<basically previous but web url>
```
