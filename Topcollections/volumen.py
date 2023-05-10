from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # Ejecución sin interfaz gráfica
options.add_argument('user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("disable-infobars")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver = webdriver.Firefox(executable_path='geckodriver', options=options)

url = "https://opensea.io/rankings?sortBy=one_hour_volume"

driver.get(url)

link = driver.find_element(By.ID, "__next")
link2 = link.find_element(By.ID, "main")
link3 = link2.find_element(By.XPATH, "//div[contains(@role, 'table')]")

data = []
tokens = []
summary = []


with open("results/nftSalesVolumeSummary.json") as jsonfile:
    summary = json.load(jsonfile)

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
