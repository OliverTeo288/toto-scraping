from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from configparser import ConfigParser

#Read config file
config_object = ConfigParser()
config_object.read('config.ini')

#Get chromedriver location
location = config_object["file location"]

driver = webdriver.Chrome(location['Chromedriver path'])
driver.get("https://www.singaporepools.com.sg/en/product/sr/Pages/toto_results.aspx?sppl=RHJhd051bWJlcj0zNjg5")

drawnoList = []
group1WSharesList = []
group1WLocList = []
group1DrawDateList = []
winningNumbers1 = []
winningNumbers2 = []
winningNumbers3 = []
winningNumbers4 = []
winningNumbers5 = []
winningNumbers6 = []
additionalNumbers = []

df = pd.DataFrame()

#Get the size of dropdown list
dropdown = driver.find_element_by_class_name("divDrawList")
totosize = len(dropdown.text.splitlines())

#Get the first value within the dropdown list
Selector = Select(driver.find_element_by_css_selector("select.form-control.selectDrawList"))
selectOptions = Selector.options
firstValue = selectOptions[len(selectOptions)-1].get_attribute('value')

group1WSharesXPath = "//*[@id='ctl00_ctl36_g_7daddb1d_8fe5_43c9_ba4a_6a00b22a7111_ctl00_divSingleResult']/div[1]/table[5]/tbody/tr[2]/td[3]"
group1WLocListXPath = [
    "//*[@id='ctl00_ctl36_g_7daddb1d_8fe5_43c9_ba4a_6a00b22a7111_ctl00_divSingleResult']/div[2]/p[2]/strong",
    "//*[@id='ctl00_ctl36_g_7daddb1d_8fe5_43c9_ba4a_6a00b22a7111_ctl00_divSingleResult']/div[2]/p[1]/strong"]
group1WLocationXPath = "//*[@id='ctl00_ctl36_g_7daddb1d_8fe5_43c9_ba4a_6a00b22a7111_ctl00_divSingleResult']/div[2]/ul[1]"
group1DrawDateXPath = "//*[@id='ctl00_ctl36_g_7daddb1d_8fe5_43c9_ba4a_6a00b22a7111_ctl00_divSingleResult']/div[1]/table[1]/thead/tr/th[1]"

#Loop throughout the list to scrape relevant data
for i in range(1, totosize + 1):
    Selector = Select(driver.find_element_by_css_selector("select.form-control.selectDrawList"))
    Selector.select_by_value(str((int(firstValue) + totosize) - i))
    drawno = driver.find_element_by_class_name("drawNumber")
    drawnoList.append(drawno.text.split(" ")[2])
    group1WShares = driver.find_element_by_xpath(group1WSharesXPath)

    if group1WShares.text != "-":
        group1WSharesList.append(group1WShares.text)
    else:
        group1WSharesList.append(0)

    try:
        group1WLocation = driver.find_element_by_xpath(group1WLocListXPath[0])
    except:
        group1WLocation = driver.find_element_by_xpath(group1WLocListXPath[1])
    finalLocDetails = ''
    # get location for each group 1 winnings
    if group1WLocation.text == "Group 1 winning tickets sold at:":
        locationlen = len(driver.find_element_by_xpath(group1WLocationXPath).text.splitlines())
        if locationlen > 1:
            for i in range(0, locationlen):
                locationdetails = driver.find_element_by_xpath(group1WLocationXPath).text.splitlines()[i]
                finalLocDetails = finalLocDetails + locationdetails + "$"
            group1WLocList.append(finalLocDetails[:-1])
        else:
            group1WLocList.append(driver.find_element_by_xpath(group1WLocationXPath).text)
    else:
        group1WLocList.append("Nil")
    group1DrawDate = driver.find_element_by_xpath(group1DrawDateXPath)
    group1DrawDateList.append(group1DrawDate.text.split(',')[1][1:])

    # winning numbers
    winningNumbers1.append(driver.find_element_by_xpath(
        "//*[@id='ctl00_ctl36_g_7daddb1d_8fe5_43c9_ba4a_6a00b22a7111_ctl00_divSingleResult']/div[1]/table[2]/tbody/tr/td[1]").text)
    winningNumbers2.append(driver.find_element_by_xpath(
        "//*[@id='ctl00_ctl36_g_7daddb1d_8fe5_43c9_ba4a_6a00b22a7111_ctl00_divSingleResult']/div[1]/table[2]/tbody/tr/td[2]").text)
    winningNumbers3.append(driver.find_element_by_xpath(
        "//*[@id='ctl00_ctl36_g_7daddb1d_8fe5_43c9_ba4a_6a00b22a7111_ctl00_divSingleResult']/div[1]/table[2]/tbody/tr/td[3]").text)
    winningNumbers4.append(driver.find_element_by_xpath(
        "//*[@id='ctl00_ctl36_g_7daddb1d_8fe5_43c9_ba4a_6a00b22a7111_ctl00_divSingleResult']/div[1]/table[2]/tbody/tr/td[4]").text)
    winningNumbers5.append(driver.find_element_by_xpath(
        "//*[@id='ctl00_ctl36_g_7daddb1d_8fe5_43c9_ba4a_6a00b22a7111_ctl00_divSingleResult']/div[1]/table[2]/tbody/tr/td[5]").text)
    winningNumbers6.append(driver.find_element_by_xpath(
        "//*[@id='ctl00_ctl36_g_7daddb1d_8fe5_43c9_ba4a_6a00b22a7111_ctl00_divSingleResult']/div[1]/table[2]/tbody/tr/td[6]").text)
    additionalNumbers.append(driver.find_element_by_xpath(
        "//*[@id='ctl00_ctl36_g_7daddb1d_8fe5_43c9_ba4a_6a00b22a7111_ctl00_divSingleResult']/div[1]/table[3]/tbody/tr/td").text)
    time.sleep(2)

df['Date'] = group1DrawDateList
df['DrawNo'] = drawnoList
df['Group 1 Winning Share'] = group1WSharesList
df['Group 1 Location'] = group1WLocList
df['Winning number 1'] = winningNumbers1
df['Winning number 2'] = winningNumbers2
df['Winning number 3'] = winningNumbers3
df['Winning number 4'] = winningNumbers4
df['Winning number 5'] = winningNumbers5
df['Winning number 6'] = winningNumbers6
df['Additional number'] = additionalNumbers
df.to_csv("data/Data.csv", index=False)

if __name__ == '__main__':
    pass
