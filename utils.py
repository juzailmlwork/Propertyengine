from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
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

def process_tab(browser):
    html_content = browser.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    mydivs1 = soup.find_all("div" ,{"class": "q3lrp5-3 cLGsWF"})
    asking_price_text=mydivs1[0].text[:]
    mydivs3 = soup.find_all("div" ,{"class": "sc-gikAfH cnigbh"})
    if len(mydivs3)!=0 and len(mydivs1)!=0:
        #try:

        if asking_price_text.count("£")==2:
            asking_price_text=asking_price_text.split("£")[2]
        else:
            asking_price_text=asking_price_text[1:]

        asking_price=int(asking_price_text.replace(',', ''))
        average_price=int(mydivs3[0].text[1:].replace(',', ''))
        #print(asking_price,average_price)
        return [asking_price,average_price]
    else:
        return False

def scrape_urls(urls):
    url_info=[]
    url_chunks = [urls[i:i+50] for i in range(0, len(urls), 50)]
    print(len(url_chunks))
    count=0
    for chunk in url_chunks:
        print(count)
        driver = create_driver()
        info={"handles":[],"urls":[]}
        #handles = []
        for url in chunk:
            url_path=f'https://propertyengine.co.uk{url}'
            driver.execute_script("window.open('{}');".format(url_path))
            info["handles"].append(driver.window_handles[-1])
            #driver.switch_to.window(info["handles"][-1])
            #url_path=f'https://propertyengine.co.uk{url}'
            driver.get(url_path)
            info["urls"].append(url_path)
        all_handles=info["handles"]
        all_urls=info["urls"]
        for index in range(len(all_handles)):
        
            driver.switch_to.window(all_handles[index])
            try:
                results=process_tab(driver)
                if results==False:
                    results=[0,0]
                bye={"url":all_urls[index],"asking_price":results[0],"average_price":results[1]}
                if results[1]-results[0]>75000:
                    print(all_urls[index])
                    print(results[0],results[1])
                url_info.append(bye)
            except:
                pass
            driver.close()
        driver.quit()
        time.sleep(10)
        count+=1
    return url_info