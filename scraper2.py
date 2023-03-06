from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from utils import create_driver
import pandas as pd

print("opening browser")
main_url=input("give me your url :")
browser=create_driver()
# Navigate to a website in the existing Chrome instance
print("opening browser")
main_url="https://propertyengine.co.uk/properties?_0:(area:ilford-greater-london,filters:!((options:(hideNewBuild:!f,hideOwnershipScheme:!t,hideRetirement:!t,hideSoldSTCRemoved:!t),type:dontShow),(options:(range:!(40000,!n)),type:askingPrice),(options:(range:!(3,4)),type:bedrooms)),sort:lowestPrice)"
number_scrolls=30
browser.get(main_url)
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "*")))
time.sleep(10)
html_content = browser.page_source
soup = BeautifulSoup(html_content, 'html.parser')

count = int(soup.find("div" ,{"class": "sc-hBxehG fyjDiA"}).find_all("span")[0].text.split(" ")[2])
print(count)
#zoom the page
#browser.execute_script("document.body.style.zoom='75%'")#150

recent_list = browser.find_element(By.XPATH, "//div[@class='sc-6jdl74-3 gjtvLs']")
number_scrolls=int(count/2)+1
# Scroll down 10 times within the div element
all_urls=[]
for i in tqdm(range(number_scrolls)):
    if i!=0:
        browser.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", recent_list)
        time.sleep(5)#5
    html_content = browser.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    mydivs = soup.find_all("a" ,{"class": "f1gc2u-0 zpUJr"})

    for element in mydivs:
        print(element["href"])
        #print(element)
        all_urls.append(element["href"])
browser.quit()

all_urls=list(set(all_urls))
print(len(all_urls))

print("opening each links")
browser=create_driver()
needed_url=[]
for link in tqdm(all_urls):
    url='https://propertyengine.co.uk{}'.format(link)
    browser.get('https://propertyengine.co.uk{}'.format(link))
    browser.execute_script("window.scrollBy(0,500)")
    #browser.execute_script("document.body.style.zoom='150%'")
    time.sleep(5)
    html_content = browser.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    mydivs1 = soup.find_all("div" ,{"class": "q3lrp5-3 cLGsWF"})
    asking_price_text=mydivs1[0].text[:]
    mydivs3 = soup.find_all("div" ,{"class": "sc-gikAfH cnigbh"})
    #print(url)
    if len(mydivs3)!=0 and len(mydivs1)!=0:
        #try:

        if asking_price_text.count("£")==2:
            asking_price_text=asking_price_text.split("£")[2]
        else:
            asking_price_text=asking_price_text[1:]

        asking_price=int(asking_price_text.replace(',', ''))
        average_price=int(mydivs3[0].text[1:].replace(',', ''))
        #print(url)
        print(asking_price,average_price)
        if average_price-asking_price>50000:#
            needed_url.append(url)
        # except:
        #     pass
    # Quit the browser
browser.quit()
print("number of results_found are",len(needed_url))
print("saving in csv file")
df = pd.DataFrame(needed_url)
df.to_csv("csv_file.csv")
print("finished")