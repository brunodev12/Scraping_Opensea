from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0"
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://opensea.io/rankings?sortBy=one_hour_volume"

driver.get(url)

link = driver.find_element(By.ID, "__next")
link2 = link.find_element(By.ID, "main")
link3 = link2.find_element(By.XPATH, "//div[contains(@role, 'table')]")

data = []
tokens = []
summary = []

def saveRawJson():
    with open("results/RawNftSalesVolume.json", "w") as jsonfile:
        json.dump(data, jsonfile)

def saveSummaryJson():
    with open("results/nftSalesVolumeSummary.json", "w") as jsonfile:
        json.dump(summary, jsonfile)


def saveElements(name_collection, _amount, _coin, _sales):
    amount = float(_amount)
    sale = int(_sales.replace('K', '000').replace(',',''))
    if name_collection not in tokens:
        tokens.append(name_collection)
        data.append({"Collection name":name_collection, "volume": amount, "coin": _coin, "Sold Amount": sale})
        saveRawJson()

def saveSummary(_summary):
    summary.append(_summary)
    if len(summary) > 24:
        summary.pop(0)
    saveSummaryJson()

def getElements(): 
    time.sleep(1)
    link4 = link3.find_elements(By.XPATH, "//a[contains(@role, 'row')]")

    for i in link4:
        print("===============================")
        text = i.text
        sep_text = text.split('\n')
        name = sep_text[1]
        price = sep_text[2]
        sales = sep_text[5]
        sep_price = price.split()
        amount = sep_price[0]
        coin = sep_price[1]
        print(f"{name} has sold {sales} NFT, for a value of {amount} {coin}")
        saveElements(name, amount, coin, sales)

while(True):
    driver.execute_script("window.scrollBy(0, 750);")
    getElements()
    last_height = driver.execute_script("return document.body.scrollHeight")
    #print("Last height", last_height)
    time.sleep(0.5)
    driver.execute_script("window.scrollBy(0, 750);")
    getElements()
    new_height = driver.execute_script("return document.body.scrollHeight")
    #print("New height", new_height)
    time.sleep(0.5)
    if last_height==new_height:
        break

total_volume = 0
total_sale_amount = 0
for i in data:
    total_volume+=i['volume']
    total_sale_amount+=i['Sold Amount']

saveSummary({"total_eth_vol": total_volume, "total_sales": total_sale_amount})

print("=============Total Volume==============")
print(total_volume)
print("=============Total Sales==============")
print(total_sale_amount)