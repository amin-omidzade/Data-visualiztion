# Ommidzadehnik   
# Last update = Jan 8 2026

# Calling essential modules

import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

import os
import re
import argparse
import warnings
import time
import seaborn as sns


# Getting webpage
try:
    webPage = input("Please enter your web page address : \t")
    
except Exception as e:
    print(e)



def userInput():
    
    # Define parser and its attribute
    parser = argparse.ArgumentParser(
        description='City, price, and type from user using command-line arguments')
    parser.add_argument('-c', '--city', type=str,
                        help='Enter the city', required=True)
    parser.add_argument('-t', '--type', type=str, choices=[
                        'buy', 'rent'], help='Enter the type (buy / rent)', required=True)
    parser.add_argument('-p', '--price', type=int,
                        help='Enter the maximum price', required=True)

    args = parser.parse_args()

    if not args.city or not args.type:
        print("Please enter city, type, and price by using --city, --type, and --price args.")
        return None, None, None

    return args.city, args.type, args.price


def urlScrap(url):
    response = requests.get(url)

    if response.status_code != 200:
        return dict()

    roomsList = list()
    priceList = list()
    spaceList = list()
    addressList = list()
    titleList = list()

    soup = BeautifulSoup(response.text, 'html.parser')

    pricesSpan = soup.find_all(
        'span', class_='HgListingCard_price_JoPAs')
    roomsSpaceDiv = soup.find_all(
        'div', class_='HgListingRoomsLivingSpace_roomsLivingSpace_GyVgq')

    addressDiv = soup.find_all(
        'div', class_='HgListingCard_address_JGiFv')

    pTag = soup.find_all(
        'p', class_='HgListingDescription_title_NAAxy')


    for i in range(len(pricesSpan)):
        # Getting numbers of price
        price = re.sub(r'\d', '', pricesSpan[i].text)
        if price:
            priceList.append(int(price))
        else:
            priceList.append(None)

        # Getting address and title
        addressList.append(addressDiv[i].text)
        titleList.append(pTag[i].text)

        # Getting room space all spans
        spanTags = roomsSpaceDiv[i].find_all('span')

        if len(spanTags) == 2:  # Available record for room and space.
            roomsText = spanTags[0].text

            # Taking text numbers
            match = re.search(r'\d+(\.\d+)?', roomsText)
            rooms = float(match.group()) if '.' in match.group() else int(
                match.group())
            roomsList.append(rooms)
            
            # Space text
            spaceText = spanTags[1].text

            # Taking text numbers
            space = re.sub(r'\D', '', spaceText)
            space = int(space)
            spaceList.append(space)

        
        elif len(spanTags) == 1: # Only data for room or space

            if 'room' in spanTags[0].text:

                roomsText = spanTags[0].text
                # Taking text numbers
                match = re.search(r'\d+(\.\d+)?', roomsText)
                rooms = float(match.group()) if '.' in match.group() else int(
                    match.group())
                roomsList.append(rooms)
                spaceList.append(None)

            elif 'space' in spanTags[0].text:

                spaceText = spanTags[0].text
                # Taking text numbers
                space = re.sub(r'\D', '', spaceText)
                space = int(space)
                roomsList.append(None)
                spaceList.append(space)

        else:  # No data
            roomsList.append(None)
            spaceList.append(None)

    data = {"rooms": roomsList, "space": spaceList,
            "price": priceList, "address": addressList,
            "title": titleList}
    
    df = pd.DataFrame(data)
    return df


def definePlots(df):
    df.sort_values(by='space', inplace=True)
    plt.figure(figsize=(14, 6))

    # Scatter plot
    plt.subplot(1, 2, 1)
    plt.scatter(df['space'], df['price'])
    plt.title('Space and Price relationship')
    plt.xlabel('Space (m^2)')
    plt.ylabel('Price')
    plt.grid(True)

    # Box plot
    sns.boxplot(x='rooms', y='price', data=df)
    plt.title(
        'Prices in Number of Rooms')
    plt.xlabel('Number of Rooms')
    plt.ylabel('Price')
    plt.tight_layout(pad=5)
    plt.show()


# Call functions
if __name__ == "__main__":
    try:
        # Delete 'Real estate.csv' file if it already exists.
        filePath = os.path.join(os.getcwd(), 'Real estate.csv')
        if os.path.exists(filePath):
            os.remove(filePath)

        # user Input
        inputCity, inputType, inputPrice = userInput()
        if inputCity and inputType and inputPrice:
            inputCity = inputCity.lower()

        
        # Define data frame
        data = {"rooms": [], "space": [],
                "price": [], "address": [], "title": []}
        finalDF = pd.DataFrame(data)

        # Ignore pandas warnings
        pd.options.mode.chained_assignment = None
        warnings.simplefilter(action='ignore', category=FutureWarning)

        page = 1
        while True:

            # parameters
            priceParam = 'aj' if inputType == 'buy' else 'ah'
            url = webPage.format(type=inputType, city=inputCity,
                                  price_param=priceParam, price=inputPrice, page=page)

            response = requests.get(url)

            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            listItems = soup.find_all('div', {'role': 'listitem'})

            if not listItems:
                break

            print(f"Extracting all recors from = {url}")

            # Scrape the url and define timer
            df = urlScrap(url)
            finalDF = pd.concat([finalDF, df], ignore_index=True)
            time.sleep(1)
            page += 1

        
        # Data preprocessing
        finalDfCleaned = finalDF.dropna(subset=['price', 'space'])
        finalDfCleaned["city"] = inputCity
        finalDfCleaned["type"] = inputType
        finalDfCleaned.to_csv('Real estate.csv', index=False)
        definePlots(finalDfCleaned)

    except Exception as e:
        print(e)
