# ClassChecker

_Updates by @au5ton:_

- Works with new 2-page CAS login that appeared in 2018
- Replaced Twilio with Telegram (because Twilio costs money and SMS sucks)
- Uses a `.env` file for sensitive information. (Shame on you @alalith for including API keys in public code!)
- Uses chromedriver instead of phantomjs
- Cleaned up source control of .exe files and junk
- Managed pip modules with a `requirements.txt` file
- Made `checker.py` an interactive tool

_Original README by @alalith:_
> ### What is this?
> This a personal project of mine, which is not meant for commericial use. This program checks if there are openings certain classes at TAMU every 10 min, and notifies me through text message. I just made this so I can check on classes while I am away from the computer

# Installation
- Install Python 3
- Install pip modules: `pip install -r requirements.txt` (make sure you're using python3's pip)
- Install and locate [Chromium](https://www.chromium.org/getting-involved/download-chromium) (not Google Chrome).
- Install and locate [Chromedriver](http://chromedriver.chromium.org/downloads). It is recommended that you install this through a package manager, like `brew` or `choco`.
- Copy `.env.example` to `.env`: `cp .env.example .env`
- Edit `.env`. CHROME_USER_DATA_DIR is important to save Duo authentication.
- Run `python checker.py --help` to learn how to use the tool
- Use the tool

# Disclosure
Sometimes this script fails because the [class search fails](img/fail.png) for no reason. I've found that it happens when there are 2 active Howdy sessions at once, so try not to use Howdy period while running this script.