from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from datetime import datetime
import pandas as pd 
import time 
import re



# Set driver options to ignore certain errors and not open a new window                      
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('headless')

url = "https://coinmarketcap.com/"

# Open webdriver and navigate to page
with webdriver.Chrome(options= chrome_options) as driver:
    driver.get(url)

    # Set values to start scrolling
    screen_height = driver.get_window_size().get("height")
    i = 1

    # Scroll to bottom of the page to load all data
    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(1)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break

    # Two functions to get the volume values separate from each other (in pandas table pull they are stuck together)
    def split_dollars():
        dollar_vol = []
        for j in range(1, 101):
            dollars = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[' + str(j) + ']/td[9]/div/a/p')
            dollar_vol.append(dollars.text)
        return dollar_vol
    
    def split_coins():
        coin_vol = []
        for j in range(1, 101):
            coins = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[' + str(j) + ']/td[9]/div/div/p')
            coin_vol.append(coins.text)
        return coin_vol
    
    # Three functions to check the color of the 1hr, 24hr and 7day columns and return a list of 'up' or 'down' values depending on green or red color
    def check_up_down_1hr():
        hr1_pos_neg = []
        for j in range(1, 101):
            color = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr['+ str(j) +']/td[5]/span')
            R_or_G = color.value_of_css_property("color")
            if R_or_G == 'rgba(234, 57, 67, 1)': 
                hr1_pos_neg.append('down')
            else: hr1_pos_neg.append("up")
        return hr1_pos_neg
    
    def check_up_down_24hr():
        hr24_pos_neg = []
        for j in range(1, 101):
            color = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr['+ str(j) +']/td[6]/span')
            R_or_G = color.value_of_css_property("color")
            if R_or_G == 'rgba(234, 57, 67, 1)': 
                hr24_pos_neg.append('down')
            else: hr24_pos_neg.append("up")
        return hr24_pos_neg
    
    def check_up_down_7d():
        d7_pos_neg = []
        for j in range(1, 101):
            color = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr['+ str(j) +']/td[7]/span')
            R_or_G = color.value_of_css_property("color")
            if R_or_G == 'rgba(234, 57, 67, 1)': 
                d7_pos_neg.append('down')
            else: d7_pos_neg.append("up")
        return d7_pos_neg

    # Function returns put in variables
    dollar_vol = split_dollars()
    coin_vol = split_coins()
    hr1_pos_neg = check_up_down_1hr()
    hr24_pos_neg = check_up_down_24hr()
    d7_pos_neg = check_up_down_7d()

    # Take html and read with pandas to find table
    df = pd.read_html(driver.page_source)



# Take html read and turn into pandas dataframe
df = pd.DataFrame(df[0])
df = df.drop(['Unnamed: 0', 'Unnamed: 11', 'Last 7 Days'], axis=1)

# Function to clean coin names
def clean_names(name):
    clean_name = re.search(r'[a-zA-Z]+', name)
    tag_name = re.search(r'\d([A-Z]+)', name)
    return (clean_name[0] + ' (' + tag_name[1] +')')

# Two functions to separate the market cap values (they were showing with the short and long values pasted together)
def separate_short_market_cap(cap):
    clean_cap = re.search(r'[$](.+)[$].+', cap)
    return clean_cap[1]

def separate_full_market_cap(cap):
    full_cap = re.search(r'[$].+([$].+)', cap)
    return full_cap[1]

# Function that takes a positive or negative list (from check up down functions above) and changes the values accordingly
def change_positive_or_negative(column, pos_neg_list):
    v_to_change = list(column.values)

    for i in range(len(v_to_change)):
        if pos_neg_list[i] == 'down':
            v_to_change[i] = '-'+ str(v_to_change[i])
    return v_to_change

# Change dataframe columns to reflect the new positive or negative value
df['1h %'] = change_positive_or_negative(df['1h %'], hr1_pos_neg)
df['24h %'] = change_positive_or_negative(df['24h %'], hr24_pos_neg)
df['7d %'] = change_positive_or_negative(df['7d %'], d7_pos_neg)

# Clean coin Names from BitcoinBTC to Bitcoin (BTC)
df['Name'] = df['Name'].apply(clean_names)

# Take 'Market Cap' column and split into two, one with abbreviated market cap and one with full market cap
df['Market Cap (full)'] = df['Market Cap']
df['Market Cap (full)'] = df['Market Cap (full)'].apply(separate_full_market_cap)
df['Market Cap'] = df['Market Cap'].apply(separate_short_market_cap)
df.rename(columns={'Market Cap' : 'Market Cap (short)'}, inplace=True)

# take volume data from page and make 2 new colums. take the column that was in the table out
df.rename(columns={'Volume(24h)' : 'Volume in $ (24h)'}, inplace=True)
df['Volume in $ (24h)'] = dollar_vol
df['Volume in coin (24h)']= coin_vol

# Re-Organise columns 
mc_col = df.pop('Market Cap (full)')
df.insert(7,'Market Cap (full)', mc_col)
vol_col = df.pop('Volume in coin (24h)')
df.insert(9 , 'Volume in coin (24h)', vol_col)


now = datetime.now()
dt_string = now.strftime("%d-%m_%H-%M")
filename = str('.\\coinprices-'+ dt_string + '.csv')
df.to_csv(path_or_buf=filename, index=False)
