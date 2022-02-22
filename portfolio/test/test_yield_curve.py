import yearfrac as yf
import matplotlib.pyplot as plt
import pandas as pd
from collections import namedtuple

def test1():
    t = list(range(1,8))
    i = [5.0, 5.375, 6.25, 6.375, 6.5, 6.51, 6.52]

    plt.figure(figsize = (20, 10))
    plt.plot(t, i)
    plt.title("Yield Curve", fontsize = 32)
    plt.xlabel("Maturity(Years)", fontsize = 18)
    plt.ylabel("Rate (%)", fontsize = 18)
    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.show()
    pass
