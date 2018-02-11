from statistics import mean
import numpy as np

def best_fit_slope_and_intercept(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
    b = mean(ys) - m*mean(xs)
    
    return m, b

# need to fetch data from db
xs = np.array([1,2,3,4,5,6,7], dtype=np.float64)
ys = np.array([151,153,154,153,152,155,157], dtype=np.float64)

m,b = best_fit_slope_and_intercept(xs,ys)
print(m,b)

regression_line = [(m*x)+b for x in xs]


# this is unnecessary. we'll render the graph with js
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

plt.scatter(xs,ys,color='#003F72')
plt.plot(xs, regression_line)
plt.show()