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

response = """\
Hello, {username}. Just a quick heads up!

It seems that you have attempted to use triple backticks (\`\`\`) for
your codeblock/monospace text block.

**This isn't universally supported on reddit**, for some users your comment
will look not as intended.

You can avoid this by **indenting every line with 4 spaces instead**.
Make sure to enter an empty line before the start of your codeblock too!

For the convenience of others, you can [view your correctly formatted
comment/submission]({url}).

Another option is the [new-reddit based codeblock](https://stalas.alm.lt/files/new-reddit-codeblock.png)
that is available through the fancy-pants editor. This also offers quite
high compatibility.

Have a good day, {username}.

^(You can opt out by replying with "backtickopt6" to this comment, send suggestions as messages)"""

opt_out_confirmation_message = """\
Hello, {username}. We are sorry to see you go. We hope you enjoyed your stay
with backtickbot.

You have requested to opt out yourself from the backtickbot service. We have successfully
processed your order.

This is a confirmation message."""

opt_out_string = "backtickopt6"

opt_out_file = "runtime/optout.json"
responded_comments_file = "runtime/responses.json"

detection_regex = "^`{3}[^\n`]{0,7}\n[^`]*^`{3}"