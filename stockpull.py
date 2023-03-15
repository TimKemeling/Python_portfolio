from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from datetime import datetime
import pandas as pd
import time

url = "https://stocktwits.com/rankings/trending"

# Open webdriver and navigate to the page
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('headless')

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
time.sleep(2)

# Find needed data and extract into list
data = driver.find_elements(By.CLASS_NAME, 'TickerTable_rankingsBodyCell__pP_NJ')

last_prices = []
for price in data:
    last_prices.append(price.text)

# Organise list to make smaller lists of data per stock
all_stock_data = []
lastIndex = 0
for i in range(len(last_prices)):
    if last_prices[i] == '':
        if lastIndex == 0:
            all_stock_data.append(last_prices[lastIndex:i])
        else: all_stock_data.append(last_prices[lastIndex +1:i])
        lastIndex = i

all_stock_data.append(last_prices[lastIndex:])
all_stock_data = all_stock_data[:-1]

# Organise data into readable structure and dataframe
stock_list = []
for stock_data in all_stock_data:
    for data in stock_data:
        stock = {
            'Number': stock_data[0],
            'Name': stock_data[1],
            'Price': stock_data[2],
            'Change ($)': stock_data[3],
            'Change (%)': stock_data[4]
        }
    stock_list.append(stock)

df = pd.DataFrame(stock_list)
driver.quit

now = datetime.now()
dt_string = now.strftime("%d-%m_%H-%M")
filename = str('.\\stocks-'+ dt_string + '.csv')
df.to_csv(path_or_buf=filename, index=False)