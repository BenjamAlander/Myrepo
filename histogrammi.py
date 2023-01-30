import sys
import matplotlib
matplotlib.use('TkAgg')

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('python-data-processing/data.csv')

df["Duration"].plot(kind="hist")

plt.show()

