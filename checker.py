import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import telegram
if os.environ["TELEGRAM_BOT_TOKEN"] is not None:
    bot = telegram.Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
import time
import urllib
import urllib.request
import urllib.parse
import platform
import datetime
import argparse
import platform
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
availableclasses=[]

IS_MACOS = platform.system() == 'Darwin' # Define boolean for if the platform is macOS or not, useful for Keys.COMMAND vs Keys.CONTROl

DEPT =     "HIST"
COURSE =   "105"
SEMESTER = "201911" # inspect element on "Search by Term" dropdown
SEMESTER_HELP = """
Semester Format: [Y]ear, [S]emester, [C]ampus as YYYYSC. 
        S = 1 if Spring, S = 2 if Summer, S = 3 if Fall. 
        C = 1 if CSTAT, C = 2 if Galveston, C = 3 if Qatar, + others. 
        Example: 201911 is Spring 2019 CSTAT. 
        """

# cli arguments
parser = argparse.ArgumentParser(epilog=SEMESTER_HELP)
parser.add_argument("-D", action="store", dest="DEPT", type=str, help="Specify DEPT as a string. Ex: HIST")
parser.add_argument("-C", action="store", dest="COURSE", type=str, help="Specify COURSE as a string. Ex: 105")
parser.add_argument("-S", action="store", dest="SEMESTER", type=str, help=f"Specify semester as a string. Ex: 201911.")
parser.add_argument("-I", action="store", dest="INTERVAL", default=300, type=int, help=f"Specify an interval between checks in seconds. Default: 300s")
parser.add_argument("--headless", action="store_true", dest="HEADLESS", default=False, help=f"Specify if program should run Chrome headless or not.")
args = parser.parse_args()
print(f"{args.DEPT} {args.COURSE} {args.SEMESTER} @ {args.INTERVAL}s (Headless: {args.HEADLESS})")

if args.DEPT is None or args.COURSE is None or args.SEMESTER is None:
    print("Must supply all arguments. See -h.")
    exit(1)
DEPT = args.DEPT
COURSE = args.COURSE
SEMESTER = args.SEMESTER
INTERVAL = args.INTERVAL
HEADLESS = args.HEADLESS

login = "https://cas.tamu.edu/cas/login?service=https://howdy.tamu.edu/uPortal/Login&renew=true"
chrome_options = Options()
if HEADLESS is True: 
    chrome_options.add_argument("--headless") # doesn't open an actual chrome window
# silences console spam
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument("user-data-dir=" + os.environ["CHROME_USER_DATA_DIR"]) # use already logged in user
chrome_options.binary_location = os.environ["CHROMIUM_BINARY"]
browser=webdriver.Chrome(executable_path=os.path.abspath(os.environ["CHROMEDRIVER_BINARY"]),   options=chrome_options)
browser.get(login)
inputElement = browser.find_element_by_id("username")
inputElement.send_keys(os.environ["TAMU_NETID"])
inputElement = browser.find_element_by_css_selector("button[type=\"submit\"]")
inputElement.click()
inputElement = browser.find_element_by_id('password')
if IS_MACOS:  # just in case password autofills
    inputElement.send_keys(Keys.COMMAND + "a")
    inputElement.send_keys(Keys.DELETE)
else:
    inputElement.send_keys(Keys.CONTROL + "a")
    inputElement.send_keys(Keys.DELETE)
inputElement.send_keys(os.environ["TAMU_PASSWORD"])
inputElement.submit()
time.sleep(3)
while True:
    searchlink = 'https://howdy.tamu.edu/uPortal/p/TAMU-APP-Launcher.ctf3/detached/render.uP?pP_targetEndpoint=bwykfcls.p_sel_crse_search'
    browser.get(searchlink)

    #browser.manage().timeouts().pageLoadTimeout(10, TimeUnit.SECONDS);
    #wait = WebDriverWait(browser, 10)
    #submit = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Submit")))

    browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
    button=browser.find_element_by_xpath('//input[@value="Submit"]')
    option=browser.find_element_by_xpath(f'//option[@value=\"{SEMESTER}\"]')
    option.click()
    button.click()
    search=browser.find_element_by_xpath('//input[@value="Advanced Search "]')
    search.click()
    option=browser.find_element_by_xpath(f'//option[@value=\"{DEPT}\"]')
    option.click()
    inputElement = browser.find_element_by_id('crse_id')
    inputElement.send_keys(COURSE)
    submit=browser.find_element_by_xpath('//input[@value="Section Search"]')
    submit.click()
    html=browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    classes = soup.find_all('tbody')[3].find_all('tr')
    classes = classes[2:]
    output=f'Here are the following available classes for {DEPT} {COURSE}:\n'
    #print(classes)
    classes_open = False # flag
    for class_ in classes:
        if "add to worksheet" in class_.find_all('td')[0].text:
            classes_open = True
            crn = class_.find_all('td')[1].text
            course = class_.find_all('td')[3].text
            section = class_.find_all('td')[4].text
            title = class_.find_all('td')[7].text
            days = class_.find_all('td')[8].text
            time_ = class_.find_all('td')[9].text
            remaining = class_.find_all('td')[12].text
            instructor = class_.find_all('td')[13].text
            availableclasses.append({'crn':crn,'course':course,'section':section,'title':title,'days':days,'time':time_,'remaining':remaining,'instructor':instructor})
            #print(availableclasses)
            output+='\t{} {}-{}, taught by {} on {} {} currently has {} seats left (CRN: {})'.format(DEPT,course.strip(),section.strip(),instructor.strip(),days.strip(),time_.strip(),remaining.strip(),crn.strip())+'\n\n'
    if not classes_open:
        output += "none"
    t = datetime.datetime.now()
    stamp = t.strftime("%m/%d/%Y @ %I:%M%p")
    print(f"[ {stamp} ] ",end="")
    print(output)
    if classes_open:
        bot.send_message(chat_id=os.environ["TELEGRAM_CHAT_ID"], text=output)
    time.sleep(INTERVAL) # wait for INTERVAL seconds (default: 5 min)
