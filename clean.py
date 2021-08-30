import pandas as pd
import requests

df = pd.read_csv("data/Data.csv")
APIfile = open("data/API key.txt", "r")
APIkey = APIfile.read()
APIfile.close()

base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

params = {
    'key': APIkey,
    'address': ''
}

response = requests.get(base_url, params=params).json()

locationdata = df[df['Group 1 Location'] != "Nil"]
newlocationdata = locationdata[~locationdata['Group 1 Location'].str.contains('iTOTO')]

newDF = pd.DataFrame()
numbersDF = pd.DataFrame()
group1Geolocation = []
totoBranch = []
category = []
subcategory = []
locations = []
newlocations = []
checklocation = []
Dates = []
filterDates = []
winningNumber = []
winningNumberdates = []

latlist = []
longlist = []
for index, row in newlocationdata.iterrows():
    locations.append(row['Group 1 Location'].split('$'))
    winningNumber.append(row['Winning number 1'])
    winningNumber.append(row['Winning number 2'])
    winningNumber.append(row['Winning number 3'])
    winningNumber.append(row['Winning number 4'])
    winningNumber.append(row['Winning number 5'])
    winningNumber.append(row['Winning number 6'])
    winningNumber.append(row['Additional number'])
    Dates.append(row['Date'])
    winningNumberdates.append(row['Date'])
    winningNumberdates.append(row['Date'])
    winningNumberdates.append(row['Date'])
    winningNumberdates.append(row['Date'])
    winningNumberdates.append(row['Date'])
    winningNumberdates.append(row['Date'])
    winningNumberdates.append(row['Date'])

for index ,i in enumerate(locations):
    for x in i:
        # checklocation.append(x.rsplit('(', 1)[0].strip())
        if (x.rsplit('(', 1)[0].strip()).split('-', 1)[1].strip() != '-':
            filterDates.append(Dates[index])
            if x.split('-')[0].strip() == '7':
                totoBranch.append(x.split('-')[0].strip() + '-' + x.split('-')[1].strip())
                newlocations.append((x.rsplit('(', 1)[0].strip()).split('-', 2)[2].strip() + ' Singapore')
                params['address'] = (x.rsplit('(', 1)[0].strip()).split('-', 2)[2].strip() + ' Singapore'

            else:
                totoBranch.append(x.split('-')[0].strip())
                newlocations.append((x.rsplit('(', 1)[0].strip()).split('-', 1)[1].strip() + ' Singapore')
                params['address'] = (x.rsplit('(', 1)[0].strip()).split('-', 1)[1].strip() + ' Singapore'
            # category.append((x.split('(')[-1][:-1].strip())[1:].strip())
            if "QuickPick" in (x.split('(')[-1][:-1].strip())[1:].strip():
                category.append('QuickPick')
                subcategory.append((x.split('(')[-1][:-1].strip())[12:].strip())
            else:
                category.append('Nil')
                subcategory.append((x.split('(')[-1][:-1].strip())[1:].strip())

            # geo coding
            response = requests.get(base_url, params=params).json()
            if response['status'] == 'OK':
               latlist.append(response['results'][0]['geometry']['location']['lat'])
               longlist.append(response['results'][0]['geometry']['location']['lng'])

newDF['Dates'] = filterDates
newDF['Branch'] = totoBranch
newDF['Group 1 Locations'] = newlocations
newDF['latitude'] = latlist
newDF['longitude'] = longlist

newDF['Category'] = category
newDF['Sub Category'] = subcategory
numbersDF['Dates'] = winningNumberdates
numbersDF['Winning number'] = winningNumber

writer = pd.ExcelWriter('data/cleanedData.xlsx')
newDF.to_excel(writer, sheet_name="Location data", index=False)
numbersDF.to_excel(writer, sheet_name="Winning Numbers", index=False)
writer.save()
