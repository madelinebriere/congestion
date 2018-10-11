import os
import numpy as np
import helper
import math
from scipy.optimize import curve_fit

def func(x, a, b):
    return a+b*np.log(x);

def plot():
    data = helper.read_list("output/data.txt")
    loss = [float(item[0]) for item in data]
    y = [float(item[1]) for item in data]
    popt, pcov = curve_fit(func, loss, y)
    y_plot = func(loss, *popt)

    popt_calc, pcov_calc = curve_fit(func, loss, np.log(y))
    print "C = %s" % -popt_calc[1]
    
    format(helper.plt)
    helper.plt.scatter(loss, y)
    helper.plt.plot(loss, y_plot, linestyle='dashed')
    helper.plt.savefig("figure_reproduced.png")

def format(plot):
    plot.xlabel("loss (%)")
    plot.ylabel("BW*RTT/MSS")
    plot.xscale('log')

if __name__ == '__main__':
    plot()