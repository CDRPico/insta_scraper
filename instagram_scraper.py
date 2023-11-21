from unicodedata import name
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import requests
import ssl
from dotenv import load_dotenv
import os

load_dotenv()
INSTAGRAM_USER = os.getenv("INSTAGRAM_USER")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

options = webdriver.ChromeOptions()
options.add_argument('--headless=false')

PATH=os.getenv("WEBDRIVER_PATH")
service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.instagram.com/")

ssl._create_default_https_context = ssl._create_unverified_context

# login
time.sleep(4)
username = driver.find_element("css selector", "input[name='username']")
password = driver.find_element("css selector", "input[name='password']")
username.clear()
password.clear()
username.send_keys(INSTAGRAM_USER)
password.send_keys(INSTAGRAM_PASSWORD)
login = driver.find_element("css selector", "button[type='submit']").click()
