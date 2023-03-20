from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

#Constantes
#url
url = "https://opensea.io/es/collection/bokinftofficial/activity?search[eventTypes][0]=AUCTION_CREATED"

#Nombres posibles de las cadenas:
'''
matic
ethereum
'''
chainName = "ethereum"

#Intervalos de tiempo posibles
'''
Última hora
Últimas 6 horas
Últimas 24 horas
Últimos 7 días
Últimos 30 días
Últimos 90 días
Todos los tiempos
'''
intervaloTiempo = "Últimas 24 horas"

#Inicio programa
driver.get(url)
driver.maximize_window()

#Rama principal
link = driver.find_element(By.ID, "__next")
link2 = link.find_element(By.ID, 'main')


#Establecer intervalo de tiempo
link3 = link2.find_element(By.XPATH, "//input[contains(@aria-invalid, 'false')][contains(@value, 'Todos los tiempos')]")
link3.click()
time.sleep(2)
link4_1 = link.find_element(By.ID, 'main')
link4_2 = link4_1.find_element(By.XPATH, "//div[@data-tippy-root]")
link5 = link4_2.find_elements(By.XPATH, f'//span[text()[contains(., "{intervaloTiempo}")]]')
link5[0].click()

#Obtener los elementos listados
link6 = link2.find_element(By.XPATH, "//div[contains(@data-testid, 'ActivityTable')]")

data = []
tokens = []

def saveJson():
    with open("listedNft.json", "w") as jsonfile:
        json.dump(data, jsonfile)

def saveElements(token_id, _priceCoin, _priceUsd):
    token_id = int(token_id)
    if token_id not in tokens:
        tokens.append(token_id)
        data.append({"token_id":token_id, "price": _priceCoin, "priceUSD": _priceUsd})
        saveJson()

def getElements():
    time.sleep(2)
    i=0
    link7 = link6.find_elements(By.XPATH, "//div[contains(@role, 'list')]")
    link8 = link7[1].find_elements(By.XPATH, "//span[contains(@data-testid, 'activity-table-item-name')]")
    for link in link7:
        if i>0:
            nftName = link8[i-1].text
            text_token = link8[i-1].get_attribute("innerHTML")[113+len(chainName):-1]
            reverse_text_token = ''.join(reversed(text_token))[60+len(nftName):-1]
            token= ''.join(reversed(reverse_text_token))
            print("=====================================")
            print(nftName, len(nftName))
            print("=====================================")
            print(text_token)
            print(token)
            link_text = link.text
            print("=====================================")
            print(link_text)
            print("=====================================")
            if link_text[0:14+len(nftName)] == f"sell\nAnunciar\n{nftName}":
                sep_text=link_text.split('\n')
                price_coin = sep_text[4]
                price_usd = sep_text[5]
                print(token)
                print(price_coin)
                print(price_usd)
                saveElements(token, price_coin, price_usd)
            else:
                print(False)
        i += 1


for j in range(300):
    driver.execute_script("window.scrollBy(0, 750);")
    getElements()
    last_height = driver.execute_script("return document.body.scrollHeight")
    print("Last height", last_height)
    time.sleep(0.5)
    driver.execute_script("window.scrollBy(0, 750);")
    getElements()
    new_height = driver.execute_script("return document.body.scrollHeight")
    print("New height", new_height)
    time.sleep(0.5)
    if last_height==new_height:
        break

for i in data:
    print(i)