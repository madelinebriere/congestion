import os
import numpy as np
import helper

def plot():
    data = helper.read_list("output/data.txt")
    loss = [float(item[0]) for item in data]
    y = [float(item[1]) for item in data]
    loss_theory = [.0001, 5]
    y_theory = [1.0/helper.math.sqrt(item) for item in loss_theory]
    
    format(helper.plt)
    helper.plt.scatter(loss, y)
    helper.plt.plot(loss_theory, y_theory, linestyle='dashed')
    helper.plt.savefig("figure_reproduced.png")

def format(plot):
    plot.xlabel("loss")
    plot.ylabel("BW*RTT/MSS")
    plot.xscale('log')

if __name__ == '__main__':
    plot()