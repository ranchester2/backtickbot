import os
import unittest
import re
import static_backtick
import backtickbot
import json


class TestDetectingMatch(unittest.TestCase):
    def check_regex(self):
        match = re.search(static_backtick.detection_regex, self.text, re.M)
        self.assertEqual(match.group(0), self.expected)

    def test_only_codeblock(self):
        self.text = """\
```cpp
We are the people of our world!
And we really hate that because we can!
Oh Oh
```"""
        self.expected = """\
```cpp
We are the people of our world!
And we really hate that because we can!
Oh Oh
```"""
        self.check_regex()

    def test_embeded(self):
        self.text = """\
Hello, we are part of the world wide health agency,
please do this
```
The past is here
but we are before
us

and why?
```

That is your answer"""
        self.expected = """\
```
The past is here
but we are before
us

and why?
```"""
        self.check_regex()

    def test_backtick_codeblock_used(self):
        text = """\
Hello, we are part of the world wide health agency,
please do this
```
The past is here
but we are before
us

and why?
```

That is your answer"""

        self.assertEqual(
            backtickbot.backtick_codeblock_used(
                static_backtick.detection_regex,
                text
            ),
            True
        )


class SimpleFilters(unittest.TestCase):
    def test_subreddit_blacklist(self):
        for subreddit in static_backtick.sub_blacklist:
            self.assertEqual(
                backtickbot.is_subreddit_blacklisted(
                    subreddit,
                    static_backtick.sub_blacklist
                ),
                True
            )

class OptOut(unittest.TestCase):
    def setUp(self):
        self.opt_out_accounts = [
            "Herbastko",
            "joe",
            "HTTP"
        ]

    
    def test_is_optout_attempt(self):
        comment = static_backtick.opt_out_string
        self.assertTrue(
            backtickbot.is_optout_attempt(
                comment,
                "amdsup",
                self.opt_out_accounts
            )
        )

        # Valid comment, but is already in list
        self.assertFalse(
            backtickbot.is_optout_attempt(
                comment,
                "Herbastko",
                self.opt_out_accounts
            )
        )

        # Not valid, user not in list
        comment = "I am not trying to opt out"
        self.assertFalse(
            backtickbot.is_optout_attempt(
                comment,
                "amdsup",
                self.opt_out_accounts
            )
        )
    
    def test_is_opted_out_with_not(self):
        author = "linux"

        self.assertFalse(
            backtickbot.is_opted_out(author, self.opt_out_accounts)
        )
    
    def test_is_opted_out_with(self):
        author = "Herbastko"

        self.assertTrue(
            backtickbot.is_opted_out(author, self.opt_out_accounts)
        )

    
    def test_opt_out_user(self):
        username = "loris"
        tmp_file_path = 'tests/tmp'

        if not os.path.exists(tmp_file_path):
            os.makedirs(tmp_file_path)
        
        with open(f'{tmp_file_path}/optout.json', 'w') as opt_out_file:
            self.assertFalse(username in self.opt_out_accounts)
            backtickbot.opt_out_user(username, self.opt_out_accounts, opt_out_file)
            self.assertTrue(username in self.opt_out_accounts)

        # Checks if file correctly saved
        
        with open(f'{tmp_file_path}/optout.json', 'r') as opt_out_file:
            self.assertEqual(json.load(opt_out_file), self.opt_out_accounts)




