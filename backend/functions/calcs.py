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

FED_URL = 'https://www.federalreserve.gov/releases/h15/'


# Opens a headless browser in chrome
def openBrowser(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--incognito')
    options.add_argument('--headless')

    # headless browser
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

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

    # Fetching all the questions on the page and storing them in questionList
    newSoup = BeautifulSoup(pageSource, 'html.parser')
    table = soup.find('table', title='Selected Interest Rates')
    tbody = table.find('tbody')
    td = tbody.find('td')
    value = td.text

    closeBrowser(browser)

    value = float(value) / 100

    return value

def closeBrowser(driver):
    driver.close()

def asset_std(values, meanReturn):
    std = 0

    for i in values["Percent_Change"]:
        std += ((meanReturn - i) ** 2)

    std /= len(values)
    std **= (1 / 2)
    return std

def nominalInterestRate():
    return daysTillStrike * ((1 + e) ^ (1 / daysTillStrike) - 1)


def randomNormal(mean, std):

    return np.random.normal(mean, std, 1)


def monte_carlo(meanReturn, std, volatility, stockPrice, days, interest):

    timeSteps = days / 252

    predPrice = 0

    for i in range(10000):
        simulationPrice = stockPrice
        for i in range(252):
            randomVariable = randomNormal(meanReturn, std)
            simulationPrice *= math.e ** ((interest - 0.5 * (volatility ** 2)) * timeSteps + volatility * (timeSteps ** (1 / 2)) * randomVariable)

        predPrice += simulationPrice

    predPrice /= 10000

    return np.round(predPrice[0], 2)


def api_call(ticker, daysTillStrike, premium, strikePrice):
    tickerSymbol = yf.Ticker(ticker)
    values = tickerSymbol.history(period="1y")

    del values['Open']
    del values['High']
    del values['Low']
    del values['Volume']
    del values['Dividends']
    del values['Stock Splits']

    dateRange = len(values)

    percentChange = [0]
    for i in range(1, dateRange):

        percentChange.append((values.iloc[i, 0] / (values.iloc[i - 1, 0])) - 1)

    values['Percent_Change'] = percentChange
    values = values.tail(-1)

    totalReturn = (values.iloc[-1, 0] / values.iloc[0, 0])
    meanReturn = (math.e ** (math.log(totalReturn) / len(values)))

    meanReturn -= 1
    std = asset_std(values, meanReturn)

    volatility = std * (len(values) ** (1 / 2))
    dateTime = 100
    stockPrice = tickerSymbol.info['regularMarketPrice']

    strikeDay = datetime.date(2023, 11, 1)
    daysTillStrike = np.busday_count(datetime.date.today() + timedelta(1), strikeDay)
    daysTillStrike /= 252

    predPrice = monte_carlo(meanReturn, std, volatility, stockPrice, daysTillStrike, fetchEffectiveRate(FED_URL))

    
    missedProfit = predPrice - stockPrice

    if missedProfit > 0:

        if missedProfit > premium:
            return("Although you will earn money off of the premium, we predict that it may be more profitable to hold the stock instead as you would make $",missedProfit," per share, instead of $",premium,".")
        
        elif missedProfit == premium:
            return("We predict that the price of the stock will increase by the same amount as the premium by the Expiry Date.")
        
        else: 
            return("Good trade! The premium you will earn is more than the predicted increase in the stock price.")



    elif missedProfit == 0:
        return("Great trade! We predict that the stock will be stagnant up until the Expiry Date and so you will make a profit of $",premium,".")



    else:

        negProfit = premium + missedProfit

        if missedProfit > premium:
            return("Although we predict that the stock price will go down by the expiry date, we still believe that you will make a profit off of this call of $",negProfit,".")
        
        elif missedProfit == premium:
            return("We predict that the price of the stock will decrease by the same amount as the premium by the Expiry Date. Therefore, although you will make a profit off of the premium, unless you intend to hold the stock in the long-term, it would probably be less stressful to sell and avoid this covered call.")

        else:
            return("Stay away from this trade. Although we believe that the option will not be exercised, we predict that the price of the stock will fall by the expiry date to the point where your overall profit will be $",negProfit".")