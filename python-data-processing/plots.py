import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('python-data-processing\data.csv')



df.plot()   # Regular Plot
df.plot(kind = "scatter", x = "Duration" , y ="Calories") # Scatter Plot
plt.show()
