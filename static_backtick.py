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
    "DimmiOuija",
    "badcode"
]

response = """\
[Correctly formatted]({url})

Hello, {username}. Just a quick heads up!

It seems that you have attempted to use triple backticks (\`\`\`) for
your codeblock/monospace text block.

**This isn't universally supported on reddit**, for some users your comment
will look not as intended.

You can avoid this by **indenting every line with 4 spaces instead**.

There are also other methods that offer a bit better compatability like
[the "codeblock" format feature on new Reddit](https://stalas.alm.lt/files/new-reddit-codeblock.png).

Tip: in new reddit, changing to "fancy-pants" editor and changing back to "markdown" will reformat correctly!
However, that may be unnaceptable to you.

Have a good day, {username}.

^(You can opt out by replying with "backtickopt6" to this comment. Configure to send allerts
to PMs instead by replying with "backtickbbotdm5". Exit PMMode by sending "dmmode_end".)"""

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
dmmode_string = "backtickbbotdm5"

opt_out_file = "runtime/optout.json"
responded_comments_file = "runtime/responses.json"
dmmode_file = "runtime/dmmode.json"

detection_regex = "(?s)^`{3}[^\n`]{0,7}\n(?:(?!```).)+^`{3}"
