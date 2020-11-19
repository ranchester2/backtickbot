import os
import unittest
import re
import static_backtick
import backtickbot
import json
from pathlib import Path
from dotenv import load_dotenv


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

    def test_embeded_backticked_word(self):
        text = """\
hello
```
the future is something `different`
which is what we love
```"""

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


class DmMode(unittest.TestCase):
    def setUp(self):
        self.dmmode_accounts = [
            "lovestone",
            "john",
            "gabmus"
        ]

    def test_is_dmmode_opt_attempt_valid(self):
        comment = static_backtick.dmmode_string
        self.assertTrue(
            backtickbot.is_dmmode_opt_attempt(
                comment,
                "valid",
                self.dmmode_accounts
            )
        )

    def test_is_dmmode_opt_attempt_already(self):
        comment = static_backtick.dmmode_string
        # Failure because already in list
        self.assertFalse(
            backtickbot.is_dmmode_opt_attempt(
                comment,
                "gabmus",
                self.dmmode_accounts
            )
        )

    def test_is_dmmode_opt_attempt_invalid(self):
        comment = "something different"
        self.assertFalse(
            backtickbot.is_dmmode_opt_attempt(
                comment,
                "gabmus",
                self.dmmode_accounts
            )
        )

    def test_dmmode_opt_user(self):
        username = "loris"
        tmp_file_path = 'tests/tmp'

        if not os.path.exists(tmp_file_path):
            os.makedirs(tmp_file_path)

        with open(f'{tmp_file_path}/dmmode.json', 'w') as dmmode_file:
            self.assertFalse(username in self.dmmode_accounts)
            backtickbot.opt_out_user(
                username, self.dmmode_accounts, dmmode_file)
            self.assertTrue(username in self.dmmode_accounts)

        # Checks if file correctly saved

        with open(f'{tmp_file_path}/dmmode.json', 'r') as dmmode_file:
            self.assertEqual(json.load(dmmode_file), self.dmmode_accounts)


class OptOut(unittest.TestCase):
    def setUp(self):
        self.opt_out_accounts = [
            "Herbastko",
            "joe",
            "HTTP"
        ]

    def test_is_opt_out_attempt_valid(self):
        comment = static_backtick.opt_out_string
        self.assertTrue(
            backtickbot.is_opt_out_attempt(
                comment,
                "amdsup",
                self.opt_out_accounts
            )
        )

    def test_is_opt_out_attempt_already(self):
        comment = static_backtick.opt_out_string
        # Valid comment, but is already in list
        self.assertFalse(
            backtickbot.is_opt_out_attempt(
                comment,
                "Herbastko",
                self.opt_out_accounts
            )
        )

    def test_is_opt_out_attempt_invalid(self):
        # Not valid, user not in list
        comment = "I am not trying to opt out"
        self.assertFalse(
            backtickbot.is_opt_out_attempt(
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
            backtickbot.opt_out_user(
                username, self.opt_out_accounts, opt_out_file)
            self.assertTrue(username in self.opt_out_accounts)

        # Checks if file correctly saved

        with open(f'{tmp_file_path}/optout.json', 'r') as opt_out_file:
            self.assertEqual(json.load(opt_out_file), self.opt_out_accounts)


class CodeblockConverter(unittest.TestCase):
    def test_converter_multi(self):
        text = """\
Hello, the solution to this problem is:
```c
int main()
{
    return 0;
}
```
That is exactly why your solution of

```
int main:
    return 0
print(f) "Hello World"
```
didn't work."""
        expected = """\
Hello, the solution to this problem is:

    int main()
    {
        return 0;
    }

That is exactly why your solution of


    int main:
        return 0
    print(f) "Hello World"

didn't work."""

        self.assertEqual(
            backtickbot.convert_text_to_correct_codeblocks(
                static_backtick.detection_regex,
                text
            ),
            expected
        )

    def test_converter_single(self):
        text = """\
hey
```
int main
dff
```"""

        expected = """\
hey

    int main
    dff
"""
        self.assertEqual(
            backtickbot.convert_text_to_correct_codeblocks(
                static_backtick.detection_regex,
                text
            ),
            expected
        )

    def test_converter_embeded_backtick(self):
        text = """\
Yes, that
```
they use a thing called `private` to fix the issue,
I don't understand it
```"""
        expected = """\
Yes, that

    they use a thing called `private` to fix the issue,
    I don't understand it
"""

        self.assertEqual(
            backtickbot.convert_text_to_correct_codeblocks(
                static_backtick.detection_regex,
                text
            ),
            expected
        )


class RemoteRestart(unittest.TestCase):
    def test_is_a_restart_attempt(self):
        restart_key = "redacted"
        self.assertTrue(
            backtickbot.is_restart_request(restart_key, restart_key)
        )

        self.assertFalse(
            backtickbot.is_restart_request("joe", restart_key)
        )

        env_path = Path('.') / 'secrets' / '.env'
        load_dotenv(dotenv_path=env_path)

        restart_key = os.environ["RESTART_KEY"]
        self.assertTrue(
            backtickbot.is_restart_request(restart_key, restart_key)
        )


class RespondedComments(unittest.TestCase):
    def setUp(self):
        self.responded_comments = [
            "12345",
            "23545",
            "54321"
        ]

    def test_is_already_responded_invalid(self):
        comment = "sdlkfjhg"
        self.assertFalse(
            backtickbot.is_already_responded(
                comment,
                self.responded_comments
            )
        )

    def test_is_already_responded_valid(self):
        comment = "12345"
        self.assertTrue(
            backtickbot.is_already_responded(
                comment,
                self.responded_comments
            )
        )

    def test_add_to_responded_comments(self):
        comment = "sdfkgjh"
        tmp_file_path = 'tests/tmp'

        with open(f'{tmp_file_path}/responses.json', 'w') as opt_out_file:
            self.assertFalse(comment in self.responded_comments)
            backtickbot.add_to_responded_comments(
                comment, self.responded_comments, opt_out_file)
            self.assertTrue(comment in self.responded_comments)

        with open(f'{tmp_file_path}/responses.json', 'r') as opt_out_file:
            self.assertEqual(json.load(opt_out_file), self.responded_comments)


class TestUsernameEscape(unittest.TestCase):
    def test_escape_username(self):
        username = "_joe_jinja*lol*"
        # Double backslash because we are fixing reddit's formatting
        # not ours.
        expected = "\\_joe\\_jinja\\*lol\\*"
        self.assertEqual(
            backtickbot.escape_username(username),
            expected
        )

#TODO: Write tests for new PREVIEW functionality, etc