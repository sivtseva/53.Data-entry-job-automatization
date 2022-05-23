import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests


google_form_link = "https://docs.google.com/forms/d/e/1FAIpQLSfesNazhaZeyAGCO-Y-2q--yVrjvu9GuGoNvD8WcqGWKoI30g/viewform?usp=sf_link"
zillow_link =  "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.69219435644531%2C%22east%22%3A-122.17446364355469%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"
headers = {
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
}
response = requests.get(url=zillow_link, headers=headers)
zillow_web_page = response.text
soup = BeautifulSoup(zillow_web_page, "html.parser")

# getting all the prices
prices_list = []
prices = soup.find_all(class_="list-card-price")
for price in prices:
    try:
        apt_price = price.getText()
        apt_price = int(apt_price.replace("$","").replace(",","").replace("/mo",""))
        prices_list.append(apt_price)
    except ValueError:
        apt_price = price.getText()
        apt_price = apt_price.split('+')
        apt_price = int(apt_price[0].replace("$","").replace(",","").replace("/mo",""))
        prices_list.append(apt_price)

# getting all the links
links_list = []
links = soup.select(".list-card-info a")
for link in links:
    href = link['href']
    if 'http' in href:
        links_list.append(href)
    else:
        href = f"https://www.zillow.com{href}"
        links_list.append(href)

# getting all the addresses
address_list = []
addresses = soup.find_all(class_='list-card-addr')
for addr in addresses:
    addr = addr.getText()
    address_list.append(addr)

# sending everything to my google form
chrome_driver_path = r"C:\Users\sivts\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
for n in range(len(address_list)):
    driver.get(google_form_link)
    time.sleep(2)
    address_form = driver.find_element(by=By.XPATH,
                                       value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_form = driver.find_element(by=By.XPATH,
                                     value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_form = driver.find_element(by=By.XPATH,
                                    value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    send_button = driver.find_element(by=By.XPATH,
                                      value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address_form.send_keys(address_list[n])
    price_form.send_keys(prices_list[n])
    link_form.send_keys(links_list[n])
    send_button.click()



