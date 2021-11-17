import sys
import requests
import wmi
import imaplib
import email
from email.header import decode_header
import webbrowser
import threading
from os.path import expanduser
import concurrent.futures
from datetime import datetime
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from os.path import expanduser
import concurrent.futures
from datetime import datetime
import time,string,zipfile,os
import random
#import selenium

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


    
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


        
def initdriver():
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
    
    driver = webdriver.Chrome(executable_path='chromedriver.exe',options=chrome_options)
    #driver.set_page_load_timeout(25)
    driver.delete_all_cookies()
    #driver.set_window_position(-10000,0)
    return driver


def changedurl(oldurl, driver):
    if oldurl in driver.current_url:
        print("Old url same as current")
        return False
    else:
        print("Old url different than current")
        return True

def collectpagetext():
    sitetext = driver.find_element_by_xpath('/html').text
    return sitetext


driver = initdriver()
oldurl = driver.current_url
while True:
    time.sleep(2)
    if changedurl(oldurl, driver) == True:
        print("Url changed")
        file = open("data.txt","a", encoding='utf-8')
        file.write(str('{'+str(collectpagetext())+'}'))
        file.close()
        oldurl = driver.current_url
        
        


