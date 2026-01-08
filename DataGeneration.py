# Omidzadehnik
# Last update = Jan 8 2026

# Calling important modules
import pandas as pd
import random

# Define 1000 Customer numbers

customerId = []

for i in range(1000):
    id = 1402100000
    customerId.append(f"{id+i+1}")

# Define products
product = {"Hat" : 1200000,
           "Shirt" : 3750000,
           "T-Shirt" : 4250000,
           "Pants" : 9800000,
           "Suit" : 43890000,
           "Socks" : 460000,
           "Tie" : 2540000,
           "Jeans" : 7410000,
           "Shoes" : 14800000,
           "Jacket" : 11000000,
           "Coat" : 22200000,
           "Boots" : 29580000}

month = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]


# Define ordder function by customer
count = 0
def buyOrder():
    global count
    count += 1
    orderNumber = f'{1402000000+count}'
    custometIdOrder = random.choice(customerId)
    productName = random.choice(list(product.keys()))
    productFee = product.get(productName)
    numberOrder = random.choice(range(1 , 11))
    discount = random.randint(0, 0.05 *(numberOrder * productFee))
    FinalPrice = numberOrder * productFee - discount
    monthOrder = random.choice(month)
    # bill = 
    bill = {"Order Number" : orderNumber,
            "Customer ID" : custometIdOrder,
            "Month order" : monthOrder,
            "Product name" : productName, 
            "Number of order" :numberOrder, 
            "Fee" : productFee,
            "Discount" : discount,
            "Final price" : FinalPrice}
    return bill

# Getting orders from customers
totalOrders = []
random.seed(222)

for j in range(10000):
    totalOrders.append(buyOrder())

# Storing in .xlsx files
totalOrdersDf = pd.DataFrame(totalOrders)
totalOrdersDf.to_excel("Botique shop.xlsx", index=None, sheet_name="Shop sale order 1402")

