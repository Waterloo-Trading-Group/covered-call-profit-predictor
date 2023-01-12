# Importing reuired libraries
import yfinance as yf
import math
import numpy as np
import datetime
from datetime import timedelta

# Webscrapping imports
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Opens a headless browser in chrome
def openBrowser(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--incognito')
    options.add_argument('--headless')

    # headless browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    driver.maximize_window()
    return driver

def fetchEffectiveRate(pageUrl):
    # Allow time for data to load
    sleepTime = 3

    browser = openBrowser(pageUrl)
    time.sleep(sleepTime)
    pageSource = browser.page_source
    # WebDriverWait(browser, 10).until(EC.title_contains("Problems - LeetCode"))

    soup = BeautifulSoup(pageSource, 'html.parser')

    #Fetching all the questions on the page and storing them in questionList
    newSoup = BeautifulSoup(pageSource, 'html.parser')
    table = soup.find('table', title='Selected Interest Rates')
    tbody = table.find('tbody')
    td = tbody.find('td')
    value = td.text

    closeBrowser(browser)

    value = float(value) / 100
    
    return value

# Closes the headless browser
def closeBrowser(driver):
    driver.close()

fedUrl = 'https://www.federalreserve.gov/releases/h15/'

print(fetchEffectiveRate(fedUrl))

# Getting the user stock and getting its ticker symbol
userStock = ''
tickerSymbol= yf.Ticker("MSFT")
values = tickerSymbol.history(period="1y")

# Deleting unneeded collumns
del values['Open']
del values['High']
del values['Low']
del values['Volume']
del values['Dividends']
del values['Stock Splits']

# Assigning the length
dateRange = len(values)

# Creating the percent change collumn
percentChange = [0]
for i in range(1, dateRange):

    percentChange.append((values.iloc[i, 0] / (values.iloc[i - 1, 0])) - 1)

values['Percent_Change'] = percentChange
values = values.tail(-1)

# print(values)

# Calculating mean return
totalReturn = (values.iloc[-1, 0] / values.iloc[0, 0])
meanReturn = (math.e ** (math.log(totalReturn) / len(values))) 

# print(math.log(totalReturn) / len(values))
# print(totalReturn)
# print(meanReturn)

meanReturn -= 1

# Asset STD function and finding overall STD
def asset_std(values, meanReturn):
    std = 0

    for i in values["Percent_Change"]:
        std += ((meanReturn - i) ** 2)
    
    std /= len(values)
    std **= (1 / 2)
    return std

std = asset_std(values, meanReturn)

volatility = std * (len(values) ** (1 / 2))
dateTime = 100
stockPrice = tickerSymbol.info['regularMarketPrice']

strikeDay = datetime.date(2023, 11, 1)
daysTillStrike = np.busday_count(datetime.date.today() + timedelta(1), strikeDay)
daysTillStrike /= 252
# print(daysTillStrike)

def nominalInterestRate():
    return daysTillStrike * ((1 + e) ^ (1 / daysTillStrike) - 1)

def randomNormal(mean, std):

    return np.random.normal(mean, std, 1)

print("hereherehere", stockPrice)

def monte_carlo(meanReturn, std, volatility, stockPrice, days, interest):

    timeSteps = days / 252

    predPrice = 0

    for i in range(10000):


        simulationPrice = float(stockPrice)


        for i in range(252):

            randomVariable = randomNormal(meanReturn, std)
            simulationPrice *= math.e ** ((interest - 0.5 * (volatility ** 2)) * timeSteps + volatility * (timeSteps ** (1 / 2)) * randomVariable)
    
        predPrice += simulationPrice
    

    predPrice /= 10000


    return np.round(predPrice[0], 2)


for i in range(10):
    print(randomNormal(meanReturn, std))

print(monte_carlo(meanReturn, std, volatility, stockPrice, daysTillStrike, fetchEffectiveRate(fedUrl)))