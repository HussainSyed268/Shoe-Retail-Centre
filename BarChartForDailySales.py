import matplotlib.pyplot as plt
import numpy as np
import random
plt.style.use('_mpl-gallery')

# make data:
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
sales = []
for day in days:
    sales.append(random.randint(5000, 50000))

fig = plt.figure(figsize=(10,5))

# plot
plt.bar(days, sales, color='maroon', width=0.4)
plt.xlabel("Days of Week")
plt.ylabel("sales")
plt.title("Weekly Summary")
plt.show()