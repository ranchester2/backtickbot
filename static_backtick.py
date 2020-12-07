sub_blacklist = [
    "anime",
    "asianamerican",
    "askhistorians",
    "askscience",
    "askreddit",
    "aww",
    "chicagosuburbs",
    "cosplay",
    "cumberbitches",
    "d3gf",
    "deer",
    "depression",
    "depthhub",
    "drinkingdollars",
    "forwardsfromgrandma",
    "geckos",
    "giraffes",
    "grindsmygears",
    "indianfetish",
    "me_irl",
    "misc",
    "movies",
    "mixedbreeds",
    "news",
    "newtotf2",
    "omaha",
    "petstacking",
    "pics",
    "pigs",
    "politicaldiscussion",
    "politics",
    "programmingcirclejerk",
    "raerthdev",
    "rants",
    "runningcirclejerk",
    "salvia",
    "science",
    "seiko",
    "shoplifting",
    "sketches",
    "sociopath",
    "suicidewatch",
    "talesfromtechsupport",
    "torrent",
    "torrents",
    "trackers",
    "tr4shbros",
    "unitedkingdom",
    "crucibleplaybook",
    "cassetteculture",
    "italy_SS",
    "DimmiOuija"
]

new_reddit_codeblock_url = "https://stalas.alm.lt/files/new-reddit-codeblock.png"

response = """\
[Fixed formatting.]({fixed_url})

Hello, {username}: code blocks using triple backticks (\`\`\`) don't work on all versions of Reddit!

Some users see [this]({incorrect_screenshot}) / [this]({incorrect_link}) instead.

To fix this, **indent every line with 4 spaces** instead.

[FAQ](https://www.reddit.com/r/backtickbot/wiki/index)

^(You can opt out by replying with {opt_out_message} to this comment.)"""

opt_out_confirmation_message = """\
Hello, {username}. We are sorry to see you go. We hope you enjoyed your stay
with backtickbot.

You have requested to opt out yourself from the backtickbot service. We have successfully
processed your order.

This is a confirmation message."""

dmmode_confirmation_message ="""\
Hello, {username}. This is a confirmation message that you have succesfully
opted for getting backtick allerts through your PM's instead."""

opt_out_string = "backtickopt6"
dmmode_string = "backtickbotdm5"

opt_out_file = "runtime/optout.json"
responded_comments_file = "runtime/responses.json"
dmmode_file = "runtime/dmmode.json"

detection_regex = "(?s)^`{3}[^\n`]{0,7}\n(?:(?!```).)+^(?:(?!```).)+^`{3}" 
