import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


with open('statistics.csv', 'r') as file:
    lines = file.readlines()

print(lines)
data = list(map(lambda line: (int(line.split(';')[0]),float(line.split(';')[1])), lines))
print(data)

# data
df=pd.DataFrame({'x': list(map(lambda x: int(x[0]), data)), 'y': list(map(lambda x: float(x[1]), data)) })
# plot
plt.plot( 'x', 'y', data=df, linestyle='-', marker='o')
plt.show()
