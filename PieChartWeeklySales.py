import matplotlib.pyplot as plt
import random
import numpy as np

# data
shoes = {"flip flop": random.randint(5000,20000), "boots":random.randint(5000,20000), "sandals":random.randint(5000,20000), "running shoes":random.randint(5000,20000)}
sales = list(shoes.values())
labels = shoes.keys()

# pie chart
plt.pie(sales, labels = labels, wedgeprops={"linewidth": 1, "edgecolor": "white"})
plt.show() 
