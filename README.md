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

Install systemd service located in data/, setup user, etc, start it.
Or just install requirements.txt and run backtickbot.py

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
```
