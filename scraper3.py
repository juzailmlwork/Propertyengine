from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import pandas as pd
import time
from bs4 import BeautifulSoup
from utils import create_driver,scrape_urls
#get input
main_url=input("give me your url :")
price_difference=int(input("give me the price difference expected :"))
browser=create_driver()
browser.get(main_url)
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "*")))
time.sleep(10)
html_content = browser.page_source
soup = BeautifulSoup(html_content, 'html.parser')

count = int(soup.find("div" ,{"class": "sc-hBxehG fyjDiA"}).find_all("span")[0].text.split(" ")[2].replace(",",""))
print("found {count} number of properties")
count=int(input("how many properties do you want to scrape maximum 4000 :"))
if count>4000:
    raise Exception
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
        #print(element["href"])
        #print(element)
        all_urls.append(element["href"])
    all_urls=list(set(all_urls))
    print(len(all_urls))
    if len(all_urls)>count:
        break
browser.quit()

#all_urls=list(set(all_urls))
print("obtained {} number of properties".format(len(all_urls)))
main_results=[]
print("scraping the properties indivdually")
all_results=scrape_urls(all_urls)
main_results.extend(all_results)
print("done scraping properties induvidually")
df = pd.DataFrame(main_results)
df2=df.loc[df["average_price"]-df["asking_price"]>price_difference]
df2.to_csv("refined_properties.csv",index=False)
print("done scraping exiting the code")