from selenium import webdriver
from selenium.webdriver.chrome.service import Service
def create_driver():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
    chrome_options.add_argument(r"--user-data-dir=C:\Users\jzlco\AppData\Local\Google\Chrome\User Data")#\Profile 4")
    chrome_options.add_argument('--profile-directory=Profile 4')
    #chrome_options.headless = True 
    service = Service("drivers/windowsdriver.exe")
    browser = webdriver.Chrome(options=chrome_options,service=service)
    return browser
def create_driver_2():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
    chrome_options.add_argument(r"--user-data-dir=C:\Users\jzlco\AppData\Local\Google\Chrome\User Data")#\Profile 4")
    chrome_options.add_argument('--profile-directory=Profile 1')
    #chrome_options.headless = True 
    service = Service("drivers/windowsdriver.exe")
    browser = webdriver.Chrome(options=chrome_options,service=service)
    return browser