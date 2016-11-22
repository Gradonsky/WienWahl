"""
Make a pie chart - see
http://matplotlib.sf.net/matplotlib.pylab.html#-pie for the docstring.

This example shows a basic pie chart with labels optional features,
like autolabeling the percentage, offsetting a slice with "explode",
adding a shadow, and changing the starting angle.

"""
from pylab import *


class Hochrechnung(object):

    def __init__(self,list):

        figure(1, figsize=(10,10))
        ax = axes([0.1, 0.1, 0.8, 0.8])

        labels = []
        fracs = []
        explode = []
        colors = ['red', 'blue', 'green', 'darkgrey', 'pink', 'white']
        r = 100
        for i in list:
            r -= i[3]
            labels.append(i[2])
            fracs.append(i[3])
            explode.append(0)

        fracs.append(r)
        explode.append(0)
        labels.append('Andere')


        pie(fracs, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=False, startangle=0)


        title('Hochrechnung', bbox={'facecolor':'1', 'pad':1})
        show()



