from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from utils import create_driver
from time import sleep

print("creating the drivers")
browser=create_driver()
# Navigate to a website in the existing Chrome instance
main_url="https://propertyengine.co.uk/properties?_0:(area:ilford-greater-london,filters:!((options:(hideNewBuild:!f,hideOwnershipScheme:!t,hideRetirement:!t,hideSoldSTCRemoved:!t),type:dontShow),(options:(range:!(40000,!n)),type:askingPrice),(options:(range:!(3,4)),type:bedrooms)),sort:lowestPrice)"
number_scrolls=4
browser.get(main_url)
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "*")))
time.sleep(5)

#zoom the page
browser.execute_script("document.body.style.zoom='150%'")

#zoom the page
#recentList =browser.find_element("xpath", "//div[@class='sc-6jdl74-3 gjtvLs']")
recent_list = browser.find_element(By.XPATH, "//div[@class='sc-6jdl74-3 gjtvLs']")

# Scroll down 10 times within the div element
all_urls=[]
for i in tqdm(range(number_scrolls)):
    browser.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", recent_list)
    time.sleep(10)#5
    html_content = browser.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    mydivs = soup.find_all("a" ,{"class": "f1gc2u-0 zpUJr"})

    for element in mydivs:
        #print(element["href"])
        all_urls.append(element["href"])
browser.quit()
sleep(5)
browser=create_driver()
all_urls=list(set(all_urls))
print(len(all_urls))

#browser=create_driver()
needed_url=[]
for link in tqdm(all_urls[:5]):
    url='https://propertyengine.co.uk{}'.format(link)
    browser.execute_script('window.open("{}", "_blank");'.format("bye"))
    sleep(1)
    browser.get(url)
    #prints parent window title
    sleep(1)
    print("Parent window title: " + browser.title)

    #get current window handle
    p = browser.current_window_handle
    print(p)

#     #get first child window
# chwd = driver.window_handles

# for w in chwd:
# #switch focus to child window
#     if(w!=p):
#     driver.switch_to.window(w)
# break
# time.sleep(0.9)
# print("Child window title: " + driver.title)
# driver.quit()

    #browser.get('https://propertyengine.co.uk{}'.format(link))
    # time.sleep(5)
    # html_content = browser.page_source
    # soup = BeautifulSoup(html_content, 'html.parser')
    # mydivs1 = soup.find_all("div" ,{"class": "q3lrp5-3 cLGsWF"})
    # mydivs3 = soup.find_all("div" ,{"class": "sc-gikAfH cnigbh"})
    # if len(mydivs3)!=0 and len(mydivs1)!=0:
    #     try:
    #         asking_price=int(mydivs1[0].text[1:].replace(',', ''))
    #         average_price=int(mydivs3[0].text[1:].replace(',', ''))
    #         print(asking_price,average_price)
    #         if average_price-asking_price>100000:
    #             needed_url.append(url)
    #     except:
    #         pass
    # Quit the browser
browser.switch_to.window(browser.window_handles[0])
sleep(1)
browser.switch_to.window(browser.window_handles[0])
sleep(1)
browser.switch_to.window(browser.window_handles[0])
sleep(1)
browser.switch_to.window(browser.window_handles[0])
sleep(1)
sleep(10)
browser.quit()