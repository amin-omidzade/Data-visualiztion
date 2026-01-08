# Omidzadehnik
# Last update = Jan 8 2026

# Imports
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def TopProducts(df):
    
    # Top 5 products
    top5Products = df.groupby('Product name')['Number of order'].sum().nlargest(5)

    # Number orders in month
    ordersInMonth = df.groupby('Month order')['Number of order'].count()

    # Final sale in month
    salesInMonth = df.groupby('Month order')['Final price'].sum()

    # Plot top 5 products
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    top5Products.plot(kind='bar', color='green')
    plt.title("Top 5 products")
    plt.xlabel("Product")
    plt.ylabel("Total Sales")

    # Plot number of orders in month
    plt.subplot(1, 3, 2)
    plt.plot(ordersInMonth.index, ordersInMonth.values, c='pink', marker='*')
    plt.title("Number of Orders in Month")
    plt.xlabel("Month")
    plt.ylabel("Number of Orders")

    # Plot final sales in month
    plt.subplot(1, 3, 3)
    plt.plot(salesInMonth.index, salesInMonth.values, c='red', marker='*')
    plt.title("Fnal of Sales in Month")
    plt.xlabel("Month")
    plt.ylabel("Sales Amount")

    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Top 5 reports.')
    parser.add_argument('-r', '--r', action='store_true', help='Top 5 reports.')
    parser.add_argument('-report', '--report', action='store_true', help='Top 5 reports.')

    args = parser.parse_args()

    try:
        # loadData
        boutiqueData = pd.read_excel("Botique shop.xlsx")

    except Exception as e:
        print(e)
        # return
    
    print(args)
    if args.report or args.r:
        # Report top5 products
        TopProducts(boutiqueData)
    else:
        print("No report given. Please write -r or --report to recieve top 5 reports.")


if __name__ == "__main__":
    main()
