import os
from twilio.rest import Client
import time
import urllib
import urllib.request
import platform
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
availableclasses=[]
account_sid = "AC8b7f3a92008d5df198de9de89dace459"
auth_token = "043be6ec5adcd4d1f6d6df95bc21b20b"
login = "https://cas.tamu.edu/cas/login?service=https://howdy.tamu.edu/uPortal/Login&renew=true"
client = Client(account_sid, auth_token)
browser=webdriver.PhantomJS("./phantomjs.exe")
browser.get(login)
inputElement = browser.find_element_by_id("username")
inputElement.send_keys('alalith')
inputElement = browser.find_element_by_id('password')
inputElement.send_keys('Lal99ith')
inputElement.submit()
while True:
    searchlink='https://howdy.tamu.edu/uPortal/p/TAMU-APP-Launcher.ctf3/detached/render.uP?pP_targetEndpoint=bwykfcls.p_sel_crse_search'
    browser.get(searchlink)

    #browser.manage().timeouts().pageLoadTimeout(10, TimeUnit.SECONDS);
    #wait = WebDriverWait(browser, 10)
    #submit = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Submit")))

    browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
    button=browser.find_element_by_xpath('//input[@value="Submit"]')
    option=browser.find_element_by_xpath('//option[@value="201731"]')
    option.click()
    button.click()
    search=browser.find_element_by_xpath('//input[@value="Advanced Search "]')
    search.click()
    option=browser.find_element_by_xpath('//option[@value="CSCE"]')
    option.click()
    inputElement = browser.find_element_by_id('crse_id')
    inputElement.send_keys('222')
    submit=browser.find_element_by_xpath('//input[@value="Section Search"]')
    submit.click()
    html=browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    classes = soup.find_all('tbody')[3].find_all('tr')
    classes = classes[2:]
    output='Here are the following available classes for CSCE 222:\n'
    for class_ in classes:
        if class_.find('abbr').text=='SR':
            crn = class_.find_all('td')[1].text
            course = class_.find_all('td')[3].text
            section = class_.find_all('td')[4].text
            title = class_.find_all('td')[7].text
            days = class_.find_all('td')[8].text
            time_ = class_.find_all('td')[9].text
            remaining = class_.find_all('td')[12].text
            instructor = class_.find_all('td')[13].text
            availableclasses.append({'crn':crn,'course':course,'section':section,'title':title,'days':days,'time':time_,'remaining':remaining,'instructor':instructor})
            output+='{}-{}, taught by {} on {} {} currently has {} seats left'.format(course,section,instructor,days,time_,remaining)+'\n\n'
    print(output)
    client.messages.create(to="+18066203600",from_="+19793143490",body=output)
    time.sleep(600)