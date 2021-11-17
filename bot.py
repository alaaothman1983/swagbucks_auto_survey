import sys
import requests
#import wmi
import imaplib
import email
from email.header import decode_header
import webbrowser
import threading
from os.path import expanduser
import concurrent.futures
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os.path import expanduser
import concurrent.futures
from datetime import datetime
import time,string,zipfile,os
#import selenium
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from threading import Thread
import threading
import base64
from PIL import Image
import cv2
    
def press_key(key, driver):
    actions = ActionChains(driver)
    actions.send_keys(key)
    actions.perform()

def randkeys(element, keys, driver):
    for myi in keys:
        element.send_keys(myi)
        time.sleep(random.uniform(0.05, 0.25))


def create_proxyauth_extension(proxy_host, proxy_port,proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    """Proxy Auth Extension
    args:
        proxy_host (str): domain or ip address, ie proxy.domain.com
        proxy_port (int): port
        proxy_username (str): auth username
        proxy_password (str): auth password
    kwargs:
        scheme (str): proxy scheme, default http
        plugin_path (str): absolute path of the extension

    return str -> plugin_path
    """
    if plugin_path is None:
        file='./chrome_proxy_helper'
        if not os.path.exists(file):
            os.mkdir(file)
        plugin_path = file+'/%s_%s@%s_%s.zip'%(proxy_username,proxy_password,proxy_host,proxy_port)

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    background_js = string.Template(
    """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "${scheme}",
                host: "${host}",
                port: parseInt(${port})
              },
              bypassList: ["foobar.com"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "${username}",
                password: "${password}"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


        
def initdriver(proxy):
    proxy = "proxy"
    print(proxy)
    chrome_options = webdriver.ChromeOptions()

    #mobilerand = random.randint(0,10)
    #useragents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
                  #,'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
                  #,'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
                  #,'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
                  #,'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1'
                  #,'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1'
                  #,'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  #,'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  #,'Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  #,'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  #,'Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  #,'Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  #,'Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  #,'Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36']
    #devicemetricslist1 = [640,
                          #480,
                          #768]
    
    #devicemetricslist2 = [1136,
                          #800,
                          #1024]

   # if mobilerand >= 3:
        #metric = random.randint(0,int(len(devicemetricslist1)-1))
        #mobile_emulation = {
            #"deviceMetrics": { "width": devicemetricslist1[metric], "height": devicemetricslist2[metric], "pixelRatio": 3.0 },
        
        #"userAgent": useragents[random.randint(0,int(len(useragents)-1))]}
        #chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    #countries = ['-country-US','-country-CA','-country-UK','-country-AU']
    therand = random.randint(0,3)
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # chrome_options.add_argument('--user-data-dir=C:\\Users\\exoti\\AppData\\Local\\Google\\Chrome\\User Data\\')
    #chrome_options.add_argument("--load-extension=C:\\Users\\exoti\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\hapgiopokcmcnjmakciaeaocceodcjdn\\6.4_0")
    #chrome_options.add_argument(str('--profile-directory=Default'))
    #chrome_options.add_argument("--start-maximized")
    #chrome_options.add_argument(str('--proxy-server='+str(proxy)))
    #chrome_options.add_argument("--headless")
    #prefs = {"profile.managed_default_content_settings.images": 2}
    #chrome_options.add_experimental_option("prefs", prefs)
    proxyauth_plugin_path = create_proxyauth_extension(
    proxy_host=str(str(proxy.split(":")[0]).strip().replace("\n","").replace("\r","")),  #"51.161.115.64",
    proxy_port=str(str(proxy.split(":")[1]).strip().replace("\n","").replace("\r","")),#80,
    proxy_username=str('user'),#+str(countries[therand])),#str(str(proxy.split(":")[2]).strip().replace("\n","").replace("\r","")),#"country-ca",
    proxy_password='passw',#str(str(proxy.split(":")[3]).strip().replace("\n","").replace("\r","")),#,
    scheme='http'
    )
    chrome_options.add_extension(proxyauth_plugin_path)
    #chrome_options.add_extension("kbfnbcaeplbcioakkpcpgfkobkghlhen.zip")
    driver = webdriver.Chrome(executable_path='chromedriver.exe',options=chrome_options)
    #driver.set_page_load_timeout(25)
    driver.delete_all_cookies()
    #driver.set_window_position(-10000,0)
    return driver


def newprofile():
    print("Not ready yet")
    age = str(random.randint(18, 35))
    
    file = open('postals.txt', 'r')
    postals = file.readlines()
    file.close()
    postal = postals[random.randint(0,int( len(postals)- 1))]

    file = open('names.txt', 'r')
    names = file.readlines()
    file.close()
    name = names[random.randint(0,int( len(names)- 1))]

    postal = postal.strip().replace("\n","").replace("\r","")
    name = name.strip().replace("\n","").replace("\r","")
    
    return str(str(age)+","+str(postal)+","+str(name))

def checkprofile(index):
    file = open(str("profiles/profile"+str(index)+".txt"), "r")
    allaccounts = file.readlines()
    file.close()

    for account in allaccounts:
        try:
            profile = str(str(account.split(":")[2]).split("|")[0])
            #acc = str(account.split(':')[0]+":"+account.split(':')[1]+":")
            age = profile.split(",")[0]
            zipcode = profile.split(",")[1]
            firstname = profile.split(",")[2]
            fullstring = str(age+","+zipcode+","+firstname)
        except Exception as Exx:
            print("Making new profile as there isn't one yet: "+str(Exx))
            profile = newprofile()
            newaccount = str(account.strip().replace("\n","").replace("\r","")+":"+profile+"\n")
            allaccounts.remove(account)
            allaccounts.append(newaccount)
            file = open(str("profiles/profile"+str(index)+".txt"),"w")
            file.writelines(allaccounts)
            file.close()
            return profile

    return fullstring

    

def register(driver,index):

    for _ in range(10):
        for _ in range(4):
            try:
                driver.get("https://cryptogmail.com/")
                break
            except Exception as EEEr:
                print("Error: "+str(EEEr))
            
        time.sleep(5)

        email = driver.find_element_by_xpath('/html/body/div/div/div[1]/div/div[1]/div').text
        #email = "jidfgfdgfdgg@accounthaven.net"
       # email = str("mrdfdfdfjohnny"+str(random.randint(9999,999999))+"@gmail.com")
        passw = str(str(email).split("@")[0])
        if len(email) >= 2:
            break
        
    print("Email: "+str(email)+" Password: "+str(passw))
    for _ in range(4):
        try:
            driver.get("https://swagbucks.com")
            break
        except Exception as EEEr:
            print("Error: "+str(EEEr))
    
    #Email
    for _ in range(10):
        try:
            randkeys(driver.find_element_by_id('sbxJxRegEmail'), email, driver)
            time.sleep(random.uniform(0.1,0.5))
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)

    #Pass
    for _ in range(10):
        try:        
            randkeys(driver.find_element_by_id('sbxJxRegPswd'), passw, driver)
            time.sleep(random.uniform(0.1,0.5))
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)
            
    #Confirm Pass
    for _ in range(10):
        try:        
            randkeys(driver.find_element_by_id('sbxJxRegEmailConfirm'), passw, driver)
            time.sleep(random.uniform(0.1,0.5))
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)

    #Submit
    for _ in range(10):
        try:      
            driver.find_element_by_xpath("//*[ contains (text(), 'Sign Up Now' ) ]").click()
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)

    time.sleep(10)


    #ACCEPT ALL
    for _ in range(3):
        try:      
            driver.find_element_by_xpath("//*[ contains (text(), 'Agree to all' ) ]").click()
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)
    
    #START EARNING
    for _ in range(3):
        try:      
            driver.find_element_by_xpath("//*[ contains (text(), 'Start Earning' ) ]").click()
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)

    for _ in range(5):
        if "onboarding" in str(driver.current_url):
            file = open(str("profiles/profile"+str(index)+".txt"),"w")
            file.write(str(email+":"+passw+"\n"))
            file.close()
            return str(email+":"+passw+"\n")
        else:
            time.sleep(1)

    
    return False


def login(driver,index):
    for _ in range(4):
        try:
            driver.get("https://www.swagbucks.com/p/login")
            break
        except Exception as EEEr:
            print("Error: "+str(EEEr))
            time.sleep(2)

    file = open(str("profiles/profile"+str(index)+".txt"),'r')
    allaccounts = file.readlines()
    file.close()

    acc = str(allaccounts[0])
    user = str(acc.split(":")[0]).strip().replace("\n","").replace("\r","")
    passw = str(acc.split(":")[1]).replace("\n","").replace("\r","")

    #user
    for _ in range(10):
        try:
            randkeys(driver.find_element_by_id('sbxJxRegEmail'),user, driver)
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)

    #pass
    for _ in range(10):
        try:
            randkeys(driver.find_element_by_id('sbxJxRegPswd'),passw, driver)
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)
            
    #submit
    for _ in range(10):
        try:
            driver.find_element_by_id('loginBtn').click()
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)

    time.sleep(40)
    #try:
    #    driver.find_element_by_xpath('//*[@id="html"]/body/div[10]/div[2]/iframe')
    #    recaptcha(driver)
    #except Exception as EEE:
    #    print("Error: "+str(EEE))
    #time.sleep(1)

def collectpagetext(driver):
    sitetext = str(driver.find_element_by_xpath('/html').text)
    return str(sitetext)
        

def clickcontextbuttons(driver, index):
    keywords = ['Male','Female']
    for _ in range(3):
        time.sleep(0.1)
        for keyword in keywords:
            try:
                print("Found element with xpath: "+str(keyword))
                #returns element found and keyword
                driver.find_element_by_xpath("//*[ contains (text(), '"+str(keyword)+"' ) ]").click()
                return
            except:
                try:
                    driver.find_element_by_xpath("//*[ contains (text(), '"+str(keyword)+"' ) ]").send_keys(Keys.SPACE)
                except Exception as EE:
                    print("Couldn't find yet context: "+str(EE))

    #GETS LIST OF ALL TAG NAMES
    try:
        try:
            inputs = driver.find_elements_by_tag_name('input')
            answers = driver.find_elements_by_tag_name('span')
            radioinputs = []
            finalanswers = []
            for input1 in inputs:
                itype = input1.get_attribute('type')
                if itype == "radio" or itype == "checkbox":
                    radioinputs.append(input1)
                    for answer in answers:
                        #if parent element is same for both elements, add to list
                       # if len(answer.text) >= 3 and "?" in str(answer.text):
                            #question = answer.text
                        if answer.find_element_by_xpath('..') == input1.find_element_by_xpath('..'):
                            finalanswers.append(str(answer.text).strip().replace("\n","").replace("\r",""))
                    print("Found radio or checkbox input")    

            question = str(driver.find_element_by_class_name('question').text)
            print(str(finalanswers))
            thing = getdataquestion(question,index)
            if thing == None:
                therand = random.randint(0,int(len(radioinputs) -1))
                radioinputs[therand].click()
                createdataquestion(question, finalanswers[therand],index)
            else:
                for i in range(finalanswers):
                    answer = finalanswers[i]
                    if thing.lower().strip() in answer.lower().strip():
                        print(str("Clicking: "+str(thing)))
                        radioinputs[i].click()
                        return
        except Exception as EEr:
            print("Error with normal context: "+str(EEr))
    
        #FOR SPECIAL WEBSITE SURVEYS researchserv 
        try:
            divs = driver.find_elements_by_tag_name('label')

            elements = []
            for div in divs:
                if "click" in str(div.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").get_attribute("class")).strip():
                    elements.append(div)

            question = str(driver.find_element_by_class_name('question-text').text) 
                    
            thing = getdataquestion(question,index)
            if thing == None:
                therand = random.randint(0,int(len(elements)-1))
                elements[therand].click()
                createdataquestion(question, elements[therand].find_element_by_xpath("/span/span[2]/label").text,index)
                print("Created new researchsav")
            else:
                for i in range(finalanswers):
                    answer = elements[i].find_element_by_xpath("/span/span[2]/label").text
                    if thing.lower().strip() in answer.lower().strip():
                        print(str("Clicking researchsav: "+str(thing)))
                        elements[i].click()
                        return
                    
        except Exception as EEe:
            print("Error with special researchsav: "+str(EEe))

        try:
            radioinputs[random.randint(0,int(len(radioinputs) -1))].send_keys(Keys.SPACE)
        except Exception as EEE:
            print("click context part 2 Error: "+str(EEE))


        #CHECKS FOR KEYWORDS
        #file = open("keywords.txt",'r')
        #keywords = file.readlines()
        #file.close()

        #for keyword in keywords:
            #thekey = keyword.strip().replace("\n","").replace("\r","")
            #time.sleep(0.1)
            
    except Exception as EEEs:
        print("Error with context: "+str(EEEs))
        #try:
        #    radioinputs[random.randint(0,int(len(radioinputs) -1))].send_keys(Keys.SPACE)
        #except Exception as EEE:
        #    print("click context part 2 Error: "+str(EEE))

def findtextinputs(driver,index):

    profile = str(checkprofile(index))
    print(profile)
    age = profile.split(",")[0]
    zipcode = profile.split(",")[1]
    name = profile.split(",")[2]
    
    keywords = ['age','zip','Age','Zip','ZIP','postal']

    pagesource = driver.page_source

    #GETS LIST OF ALL TAG NAMES
    found = False
    for _ in range(3):
        time.sleep(0.1)
        inputs = driver.find_elements_by_tag_name('input')
        textinputs = []
        for input1 in inputs:
            itype = input1.get_attribute('type')
            if itype == "text" or itype == "number":
                textinputs.append(input1)
                print("Found text input")
                found = True
        if found == True:
            break

    #LOOP KEYWORDS, IF KEYWORD FOUND, ENTER CONTEXT ANSWER
    for keyword in keywords:
        try:
            print(str(collectpagetext(driver).lower()))
            if keyword in collectpagetext(driver).lower():
                if keyword == "age" or keyword == "Age":
                    print("Found age keyword")
                    #SEND AGE TO FIRST INPUT
                    if (int(len(textinputs)-1)) >= 1:
                        for i in range(int(len(textinputs)-1)):
                            try:
                                randkeys(textinputs[i],age,driver)
                                print("Wrote into text input")
                                break
                            except Exception as EEe:
                                print("Error: "+str(EEe))
                    else:
                        try:
                            randkeys(textinputs[0],age,driver)
                            print("Wrote into text input")
                            break
                        except Exception as EEe:
                            print("Error: "+str(EEe))
                            
                if keyword == "zip" or keyword == "Zip" or keyword == "ZIP" or keyword == "postal":
                    print("Found age keyword")
                    #SEND ZIP TO FIRST INPUT (CHANGE LATER)
                    if (int(len(textinputs)-1)) >= 1:
                        for i in range(int(len(textinputs)-1)):
                            try:
                                randkeys(textinputs[i],zipcode,driver)
                                print("Wrote into text input")
                                break
                            except Exception as EEe:
                                print("Error: "+str(EEe))
                    else:
                        try:
                            randkeys(textinputs[0],zipcode,driver)
                            print("Wrote into text input")
                            break
                        except Exception as EEe:
                            print("Error: "+str(EEe))
                    
        except Exception as EEE:
            print("Error: "+str(EEE))

    

def firstsurvey(driver,index):
    #Click first offer
    link = ""
    for _ in range(10):
        try:     
            link = driver.find_element_by_xpath("//*[ contains (text(), 'Complete your profile survey' ) ]").get_attribute('href')
            break
        except:
            try:
                link = driver.find_element_by_xpath("//*[ contains (text(), 'Take this survey' ) ]").get_attribute('href')
            except Exception as EEE:
                print("Exception: "+str(EEE))
                time.sleep(1)
    for _ in range(4):
        try:
            driver.get(link)
            break
        except Exception as EEEr:
            print("Error: "+str(EEEr))

    time.sleep(5)
    while True:
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//*[ contains (text(), 'Verify with Text' ) ]")
            driver.get("https://swagbucks.com/suveys")
            print("Returning")
            return
        except Exception as EE:
            print("Exception: "+str(EE))
        clickcontextbuttons(driver,index)
        findtextinputs(driver, index)
        dropdown(driver, index)
        clicksubmit(driver)
        
        

def checkstatus(driver):
    keywords = ['Your next gift card is just a few clicks away!','Swagbucks Answer','Answer Gold Surveys']
    status = ['onboarding','surveyscreen','surveyscreen']
    for i in range(int(len(keywords) - 1)):
        try:
            if str(keywords[i]) in collectpagetext(driver):
                return str(status[i])
        except Exception as EE:
            print("Error: "+str(EE))
        
    return "None"


def clicksubmit(driver):
    keywords = ['Submit','Continue','Go','Next',">>",">"]
    for _ in range(3):
        time.sleep(0.1)
        for keyword in keywords:
            try:
                driver.find_element_by_xpath("//*[ contains (text(), '"+str(keyword)+"' ) ]").click()
                return
            except Exception as EE:
                print("Couldn't find yet: "+str(EE))

    for _ in range(3):
        time.sleep(0.1)
        for keyword in keywords:
            try:
                allinputs = driver.find_elements_by_tag_name('input')
                for inp in allinputs:
                    if keyword in inp.get_attribute('value'):
                        inp.click()
                        return
            except Exception as EE:
                print("Error: "+str(EE))

    #Failsafe
    #try:
        #allforms = driver.find_elements_by_tag_name("form")
        #for form in allforms:
            #form.submit()
    #except Exception as EEe:
     #   print("Error: "+str(EEe))

def dropdown(driver, index):
    profile = str(checkprofile(index))
    print(profile)
    age = profile.split(",")[0]
    #zipcode = profile.split(",")[1]
    #name = profile.split(",")[2]
    
    keywords = ['Month','Year','Day','Select one']
    sub1 = ['May','Jun','Jul','Dec','Jan','Sep','Aug','Nov']
    sub2 = ['1','2','3','4','5','6','7','8','9','10','11']
    for _ in range(3):
        time.sleep(0.1)
        for keyword in keywords:
            try:
                print("Found dropdown with xpath: "+str(keyword))
                #returns element found and keyword
                driver.find_element_by_xpath("//*[ contains (text(), '"+str(keyword)+"' ) ]").click()
                time.sleep(random.uniform(0.8, 1.0))
                if keyword == "Month":
                    driver.find_element_by_xpath("//*[ contains (text(), '"+str(sub1[random.randint(0,int(len(sub1) - 1)) ])+"' ) ]").click()
                    time.sleep(random.uniform(0.1,0.2))
                    return
                if keyword == "Year":
                    driver.find_element_by_xpath("//*[ contains (text(), '"+str(int(2021 - int(age)))+"' ) ]").click()
                    time.sleep(random.uniform(0.1,0.2))
                    return
                if keyword == "Day":
                    driver.find_element_by_xpath("//*[text() = '"+str(sub2[random.randint(0,int(len(sub2) - 1)) ])+"']").click()
                    time.sleep(random.uniform(0.1,0.2))
                    return
                if keyword == "Select one":
                    element = driver.find_element_by_xpath("//*[ contains (text(), 'Select one' ) ]")
                    element.click()
                    children = element.find_elements_by_tag_name('option')
                    children[random.randint(0, int(len(children) - 1) ) ].click()    
                    
                    time.sleep(random.uniform(0.1,0.2))
                    return
                
            except Exception as EE:
                print("Couldn't find yet: "+str(EE))
        try:
            elements = driver.find_elements_by_tag_name("select")
            for element in elements:
                try:
                    options = element.find_elements_by_tag_name("option")
                    options[random.randint(0,int(len(options)-1))].click()
                except Exception as Ee:
                    print("Error finding dropdown elements: "+str(Ee))
        except Exception as Ee:
            print("Error: "+str(Ee))
    

def verifyemail(driver, reg, index):
    
    for _ in range(4):
        try:
            driver.get("https://cryptogmail.com/")
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
    time.sleep(0.1)
    for _ in range(15):
        press_key(Keys.DOWN,driver)
        time.sleep(0.4)
    for _ in range(10):
        try:
            driver.find_element_by_xpath("//*[ contains (text(), 'info@swagbucks.com' ) ]").click()
            time.sleep(0.2)
            driver.find_element_by_xpath("//*[ contains (text(), 'info@swagbucks.com' ) ]").click()
            time.sleep(1)            
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)
    time.sleep(10)
    for _ in range(10):
        press_key(Keys.DOWN,driver)
        time.sleep(0.4)
    #FINISH
    for _ in range(10):
        try:
            link = driver.find_element_by_xpath("//*[ contains (text(), 'Confirm Email Address' ) ]").get_attribute('href')
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)

    try:
        driver.get(link)
        #SAVES ACCOUNT ONLY IF IT WORKED
    except:
        print("unable to get link, returning false")
        return False

    #BACK TO HOME
    for _ in range(10):
        try:
            driver.find_element_by_xpath("//*[ contains (text(), 'Take me to the homepage.' ) ]").click()
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)
    

    time.sleep(10)

    driver.get("https://swagbucks.com/surveys")

    #Go now        
    for _ in range(10):
        try:
            driver.find_element_by_xpath("//*[ contains (text(), 'Go Now' ) ]").click()
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)

    #I PROMISE TO ANSWER CHECKBOX
    press_key(Keys.PAGE_DOWN, driver)
    for _ in range(10):
        try:
            driver.find_element_by_xpath("//*[ contains (text(), 'I promise to answer survey questions honestly.' ) ]").click()
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(1)
    press_key(Keys.PAGE_DOWN, driver)
    clicksubmit(driver)

    time.sleep(2)

    
    for _ in range(10):
        try:
            element = driver.find_element_by_xpath("//*[ contains (text(), 'Complete The Basics First' ) ]").text
            return False
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(0.5)

    
    file = open(str("profiles/profile"+str(index)+".txt"),"a")
    file.write(reg)
    file.close()
    return True


def completesurveys(driver, index):
    #Click first offer
    print("-----------------STARTING NORMAL SURVEY LOOP-------------------")
    link = ""
    driver.get("https://swagbucks.com/surveys")
    #I PROMISE TO ANSWER CHECKBOX
    time.sleep(3)
    press_key(Keys.PAGE_DOWN, driver)
    for _ in range(10):
        try:
            driver.find_element_by_xpath("//*[ contains (text(), 'I promise to answer survey questions honestly.' ) ]").click()
            break
        except Exception as EEE:
            print("Error: "+str(EEE))
            time.sleep(0.1)
    press_key(Keys.PAGE_DOWN, driver)
    clicksubmit(driver)
    for _ in range(10):
        try:     
            link1 = driver.find_element_by_xpath('//*[@id="surveyList"]/tbody[4]/tr[1]/td[4]/a').get_attribute('onclick')
            link1 = str(link1.split("return surveyClick(this, '")[1].split("',")[0].strip())
            link  = str("https://swagbucks.com"+str(link1))
            break
        except Exception as EE:
            print("Exception: "+str(EE))
            time.sleep(0.1)
    for _ in range(4):
        try:
            driver.get(link)
            break
        except Exception as EEEr:
            print("Error: "+str(EEEr))
    time.sleep(4)
    while True:
        time.sleep(2) 
        try:
            driver.find_element_by_xpath("//*[ contains (text(), 'Start Survey' ) ]")
            driver.get("https://swagbucks.com/surveys")
            print("Returning")
            return
        except Exception as EE:
            print("Exception: "+str(EE))
        clickcontextbuttons(driver,index)
        findtextinputs(driver, index)
        dropdown(driver, index)
        clicksubmit(driver)


def captcha(driver,index):

    key = "2captchakeyhere"
    #cookies = {'AWSALBCORS':'GsunlYJhUTO0tUJOOy2xtAcMRYmKszZzCmCgJCZDUFvSiHDkbL73TeK9SWdt1iKg3oVHMnjBHDeIhfTs7iIa/9gjba1JQsK4l/KTz0HzjsN+mNvmQe1hYTNczfVB','AWSALB':'GsunlYJhUTO0tUJOOy2xtAcMRYmKszZzCmCgJCZDUFvSiHDkbL73TeK9SWdt1iKg3oVHMnjBHDeIhfTs7iIa/9gjba1JQsK4l/KTz0HzjsN+mNvmQe1hYTNczfVB','_hp2_id.715588404':'%7B%22userId%22%3A%228507714292604552%22%2C%22pageviewId%22%3A%227618944432711688%22%2C%22sessionId%22%3A%228526999139391128%22%2C%22identity%22%3A%22109508438%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%2C%22oldIdentity%22%3Anull%7D'}
    #response = requests.get(src, headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}, cookies=cookies)
    driver.get_screenshot_as_file(str("captcha"+str(index)+".png"))
    #if response.status_code == 200:
        #with open(str("captcha"+str(index)+".jpg"), 'wb') as f:
           # f.write(response.content)
    img = cv2.imread(str("captcha"+str(index)+".png"))
    crop_img = img[300:300+190, 200:200+500]
    cv2.imwrite(str("captcha"+str(index)+".png"),crop_img)
    cv2.waitKey(0)
    time.sleep(1)
    #with open(str("captcha"+str(index)+".png"), "rb") as img_file:
        #my_string = base64.b64encode(img_file.read())
    #my_string = str(my_string).strip().replace("b'","").replace("'","")
    #print(my_string)
    for _ in range(3):
        try:
            files = {'file': open(str("captcha"+str(index)+".png"), 'rb')}
            data = {'key': key, 'method': 'post','textinstructions':'"Find the captcha in the picture and enter the captcha letters ONLY (3 letters)"'}
            response = requests.post("http://2captcha.com/in.php",data=data, files=files)
            print(response.text)
            if "OK" in str(response.text):
                theid = str(response.text).split("|")[1].strip().replace("\n","").replace("\r","")
                break
        except Exception as EE:
            print("error: "+str(EE))
            time.sleep(1)

    print(theid)
    time.sleep(15)

    for _ in range(90):
        try:
            response = requests.get(str("http://2captcha.com/res.php?key="+str(key)+"&action=get&id="+str(theid)))
            print(response.text)
            if "OK" in str(response.text):
                answer = str(response.text).split("|")[1].strip().replace("\n","").replace("\r","")
                return answer
            else:
                time.sleep(1)
        except Exception as EE:
            print("error: "+str(EE))
            time.sleep(1)

    
    

def search(driver,index):
    
    file = open("searches.txt","r")
    searches = file.readlines()
    file.close()

    driver.get("https://swagbucks.com")
    for search in searches:
        try:
            for _ in range(10):
                try:
                    #randkeys(driver.find_element_by_id('sbGlobalNavSearchInputWeb'),search,driver)
                    thesearch = str(str(search).strip().replace("\n","").replace("\r","")+"+"+str(searches[random.randint(0,int(len(searches)-1)) ]).strip().replace("\n","").replace("\r",""))
                    driver.get(str("https://www.swagbucks.com/?f=11&q="+str(thesearch)))
                    time.sleep(random.uniform(0.5, 0.7))
                    #press_key(Keys.ENTER, driver)
                    break
                except Exception as EEr:
                    print("Error: "+str(EEr))

            time.sleep(2)

            for _ in range(random.randint(2,9)):
                press_key(Keys.PAGE_DOWN, driver)
                time.sleep(random.uniform(0.2, 1.2))

            for _ in range(random.randint(2,9)):
                press_key(Keys.PAGE_UP, driver)
                time.sleep(random.uniform(0.2, 1.2))
                    
            for _ in range(10):
                #CHECK SUCCESSFUL SEARCH EARN
                try:
                    driver.find_element_by_xpath("//*[ contains (text(), 'Your search just earned' ) ]").text
                    file = open("successfulsearches.txt","a")
                    file.write(str(str(thesearch)+"\n"))
                    file.close()
                    #CHECK SUCCESSFUL SEARCH EARN
                    for _ in range(10):
                        try:
                            imglink = str(driver.find_element_by_id("captchaImg").get_attribute('src'))
                            break
                        except Exception as EE:
                            print("Error searching: "+str(EE))

                    code = str(captcha(driver,index))
                    for _ in range(10):
                        try:
                            randkeys(driver.find_element_by_class_name('catpthcaInput'),str(code),driver)
                            break
                        except Exception as EEEe:
                            print("Error: "+str(EEEe))

                    time.sleep(0.4)
                    try:
                        press_key(Keys.ENTER, driver)
                    except:
                        print("Error clicking enter")

                    try:
                        driver.find_element_by_class_name('catpthcaInput').send_keys(Keys.ENTER)
                    except:
                        print("Error clicking enter")
                        
                    time.sleep(1)
                    break
                    
                except Exception as EE:
                    print("Error finding reward: "+str(EE))
                    time.sleep(0.1)


            time.sleep(random.randint(5,10)) 
                
        except Exception as EEEE:
            print("Error: "+str(EEEE))


def recaptcha(driver):
    #RECAPTCHA
        key = "2capchakeyhere"
        for _ in range(10):
            try:
                response = requests.get(str("http://2captcha.com/in.php?key="+str(key)+"&googlekey=6Ld48JYUAAAAAGBYDutKlRp2ggwiDzfl1iApfaxE&method=userrecaptcha&pageurl=https://www.swagbucks.com/p/login"))
                if "OK" in str(response.text):
                    captchakey = str(response.text).split("|")[1].strip().replace("\n","").replace("\r","")
                    print(str("Got first key: "+str(captchakey)))
                    breakl = False
                    break
                time.sleep(1)
           
            except Exception as EEEE:
                print("Error: "+str(EEEE))
                time.sleep(1)
             

   
        time.sleep(15)

        for _ in range(90):
            try:
                response = requests.get(str("http://2captcha.com/res.php?key="+str(key)+"&action=get&id="+str(captchakey)))
                print(response.text)
                if "OK" in str(response.text):
                    finalkey = str(response.text).split("|")[1].strip().replace("\r","").replace("\n","")
                    print(str("Got final key: "+str(finalkey)))
                    breakl = False
                    break
                time.sleep(1)
                
            except Exception as EXR:
                print("Waiting for response: "+str(EXR))
                time.sleep(1)
           

        #g-recaptcha-response
        driver.execute_script(str('document.getElementById("g-recaptcha-response").innerHTML="'+str(finalkey)+'";'))

        time.sleep(1)

        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="html"]/body/div[10]/div[2]/iframe'))
        driver.find_element_by_id('recaptcha-token').submit()
        driver.switch_to.default_content()
        time.sleep(1)
#MAKE VERIFICATION FOR EMAILS
def main(index,proxy):
    while True:
        try:
            driver = initdriver(proxy)

            allaccounts = os.listdir("profiles")
            reg = None
            breakl = False
            if len(allaccounts) >= 1:
                login(driver,index)
            else:
                reg = register(driver,index)
                if reg == False:
                    print("Breakl true")
                    breakl == True

            if breakl == False:
            
                while True:
                    for _ in range(5):
                        try:
                            status = checkstatus(driver)
                            if status != "None":
                                break
                            else:
                                time.sleep(0.05)
                        except Exception as EEE:
                            print("Looking for status: "+str(EEE))

                    try:
                        if status == "onboarding" and reg != None:
                            time.sleep(1)
                            firstsurvey(driver,index)
                            if verifyemail(driver, reg, index) == False:
                                break
                        else:
                            time.sleep(1)
                            completesurveys(driver,index)
                            #search(driver,index)
                    except Exception as EEe:
                        print("Error: "+str(EEe))
            try:
                driver.close()
                driver.quit()
            except:
                print("Didn't close driver properly")

            os.system(str("curl -x "+str(proxy)+" -U username http://api.proxyrack.net/release"))
                        
        except Exception as EE:
            print("Error: "+str(EE))


#Checks for data question saves
def getdataquestion(question, index):
    try:
        thestr = str(question.strip().replace('\n',"").replace('\r',"").replace(':',""))
        
        file = open(str("profiles/profile"+str(index)+".txt"),"r")
        theprofile = str(file.read()).strip().replace("\n","").replace("\r","")
        file.close()

        elements = str(theprofile).split("|")
        elements.remove(elements[0])

        for element in elements:
            if thestr in str(element):
                return str(element).split(";")[1].strip().replace("\n","").replace("\r","")

        return None
        
    except Exception as EE:
        print("Error: "+str(EE))
            

def createdataquestion(question, answer, index):
    try:
        thestr = str(question.strip().replace('\n',"").replace('\r',"").replace(':',""))
        answer = str(answer.strip().replace('\n',"").replace('\r',"").replace(':',""))
        
        file = open(str("profiles/profile"+str(index)+".txt"),"r")
        theprofile = str(file.read()).strip().replace("\n","").replace("\r","")
        file.close()

        theprofile = str(theprofile+"|"+str(thestr)+";"+str(answer))
        
        file = open(str("profiles/profile"+str(index)+".txt"),"w",encoding='utf8')
        file.write(theprofile)
        file.close()
        return True
    except Exception as EE:
        print("Error getting dataset main: "+str(EE))
        return False        

def threads(amnt):

    threads = []
    file = open("proxies.txt","r")
    proxies = file.readlines()
    for i in range(amnt):
        threads.append(threading.Thread(target=main,args=[i,proxies[i],]))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


print("""************************************************************
ADVANCED AUTO ADAPTING SURVEY BOT V.1 (BETA)
************************************************************
ARGS
threads - Amount of surveys to solve at once
************************************************************

""")
########################################################
#!IMPORTANT
#----------------
#TO DO
#----------------
#-Do keyword magic with dataquestion storing functions
#
#
#
#
#######################################################
while True:
    try:
        amnt = int(str(input("Amount of threads: ")).strip())
        break
    except:
        print("Not an integer")
        
threads(int(amnt))






