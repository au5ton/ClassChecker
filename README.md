# ClassChecker

_Updates by @au5ton:_

I've updated the software to work with the new CAS login, as well as some other tweaks.

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