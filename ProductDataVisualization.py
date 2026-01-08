# Omidzadehnik
# Last Update = Jan 8 2026

# Import essential libraries

import pandas as pd
from matplotlib import pyplot as plt

# Reading data set
try:
    boutiquedf = pd.read_excel("Botique shop.xlsx") 

except Exception as e:
    print(e)

# Getting name of Products in lower
with pd.option_context('mode.chained_assignment', None):
    for i in range(len(boutiquedf["Product name"])):
        boutiquedf["Product name"][i] = boutiquedf["Product name"][i].lower()

# Getting name of product

productInput = input("Please enter your product name!").lower()

# Taking all products sale
productSaleStat = boutiquedf.where(boutiquedf["Product name"] == productInput).dropna()

if productSaleStat.empty:
    print("Your product is not in the list!")

else:
    print(f"Cool! You select {productInput}")

    # Number of orders for each month
    numberOfOrderInMonth = productSaleStat.groupby("Month order")["Number of order"].sum()

    # Define bar graph for sales
    plot1 = plt.figure()
    plt.bar(numberOfOrderInMonth.index, numberOfOrderInMonth, color="#4CAF50")
    plt.xlabel("Month")
    plt.ylabel("Number of sales")
    plt.title(f"Sales number of {productInput} in each month")

    # Fluctuation of price of the product after discount (Final price) and recalcualte the fee
    averageOfPriceInMonth = productSaleStat.groupby("Month order")["Final price"].sum() / productSaleStat.groupby("Month order")["Number of order"].sum()
    
    # Define line graph for sale changes
    plot2 = plt.figure()
    plt.plot(averageOfPriceInMonth.index, averageOfPriceInMonth, color = "purple")
    plt.xlabel("Month")
    plt.ylabel("price")
    plt.title(f"Average price of {productInput} in each month")
    plt.show()
