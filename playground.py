import numpy as np
import pandas as pd


data = {
    'calories': [420,380,201],
    'duration': [50,40,45]
}

myvar = pd.DataFrame(data, index = ['day1','day2','day3'])
print(myvar)

print(myvar.loc['day2'])