# Omidzadehnik
# Jan 27 2026

# Import essential libraries

import pandas as pd
import matplotlib.pyplot as plt

# Reading data set
try:
    boutiquedf = pd.read_excel("Botique shop.xlsx") 

except Exception as e:
    print(e)

# Getting ID of ucstomers Example : 1402100330 (True)

customerIDInput = int(input("Please enter your customer ID!"))

# Taking all customers purchases
customerBuyStat = boutiquedf.where(boutiquedf["Customer ID"] == customerIDInput).dropna()

if customerBuyStat.empty:
    print("This customer is not in the list!")

else:
    print(f"OK! You select {customerIDInput}")

    # Number of all purcheses for each month
    numberOfPurchesInMonth = customerBuyStat.groupby("Month order")["Order Number"].count()

    # Define bar graph for all purcheses for each month
    plot1 = plt.figure()
    plt.bar(numberOfPurchesInMonth.index, numberOfPurchesInMonth, color="#4CAF50")
    plt.xlabel("Month")
    plt.ylabel("Number of Purchases")
    plt.title(f"Purches number of customer {customerIDInput} in each month")

    # Total price purcheses for each month
    totalPurchesInMonth = customerBuyStat.groupby("Month order")["Final price"].sum()

    # Define scatter plot for total price purcheses for each month
    plot2 = plt.figure()
    plt.scatter(totalPurchesInMonth.index, totalPurchesInMonth)
    plt.xlabel("Month")
    plt.ylabel("Purchases price")
    plt.title(f"Total purches price of customer {customerIDInput} in each month")

    # Total purcheses for each product
    totalPurchesProduct = customerBuyStat.groupby("Product name")["Product name"].count()

    # Define bar plot for all purcheses for each product
    plot3 = plt.figure()
    plt.bar(totalPurchesProduct.index, totalPurchesProduct)
    plt.xlabel("Product")
    plt.ylabel("Purchases number")
    plt.title(f"Total purches of customer {customerIDInput} for each product")
    plt.show()
    
