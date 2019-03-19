# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 12:48:01 2019

@author: F900591
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot, pylab


txcc = pd.read_csv('./csv/TXFCC-Minute-Trade.txt', date_parser = 'Date')
txcc['DateTime'] = pd.to_datetime(txcc['Date'] + " " + txcc['Time'])
txcc.set_index("DateTime" , inplace=True)
txcc['TXCC'] = txcc['Close']
filtertxcc = (txcc['Time'] == '13:30:00')
txcc = txcc[filtertxcc]
txcc['TX'] = (txcc['Close'].shift(-10) - txcc['Close'].shift(0))/txcc['Close'].shift(0)*100
txcc = txcc.dropna()

twmc = pd.read_csv('./csv/TW-MC-Minute-Trade.txt', date_parser = 'Date')
twmc['DateTime'] = pd.to_datetime(twmc['Date'] + " " + twmc['Time'])
twmc.set_index("DateTime" , inplace=True)
twmc['TWMC'] = twmc['Close']
filtertwmc = (twmc['Time'] == '13:30:00')
twmc = twmc[filtertwmc]
twmc = twmc.dropna()

stwc1 = pd.read_csv('./csv/STWC1-Minute-Trade.txt', date_parser = 'Date')
stwc1['DateTime'] = pd.to_datetime(stwc1['Date'] + " " + stwc1['Time'])
stwc1.set_index("DateTime" , inplace=True)
stwc1['STWC1'] = stwc1['Close']
filterstwc1 = (stwc1['Time'] == '13:30:00')
stwc1 = stwc1[filterstwc1]
stwc1 = stwc1.dropna()

stwmc = pd.read_csv('./csv/STW-MC-Minute-Trade.txt', date_parser = 'Date')
stwmc['DateTime'] = pd.to_datetime(stwmc['Date'] + " " + stwmc['Time'])
stwmc.set_index("DateTime" , inplace=True)
stwmc['STWMC'] = stwmc['Close']
filterstwmc = (stwmc['Time'] == '13:30:00')
stwmc = stwmc[filterstwmc]
stwmc = stwmc.dropna()

tw = pd.read_csv('./csv/TW.csv', date_parser = 'Date')
tw['Date'] = tw['Date'] + " 13:30:00"
tw.set_index("Date" , inplace=True)
tw.index = pd.to_datetime(tw.index)
tw['STW'] = (tw['Close'].shift(-10) - tw['Close'].shift(0))/tw['Close'].shift(0)*100
tw = tw.dropna()



stwfData = pd.concat([txcc['TXCC'], twmc['TWMC'], stwc1['STWC1']
            , stwmc['STWMC'], txcc['TX'], tw['STW']], axis=1).astype(np.float)
stwfData = stwfData.dropna()



stwfData['basis'] = (((stwfData['STWC1'] - stwfData['STWMC'])/
        stwfData['STWMC'])-((stwfData['TXCC'] - stwfData['TWMC'])/stwfData['TWMC']))*100

fig = pyplot.figure(figsize=(14, 8))
ax1 = pyplot.subplot(221)
ax2 = pyplot.subplot(222)
ax3 = pyplot.subplot(223)
ax4 = pyplot.subplot(224)

ax1.grid(True)
ax1.scatter(stwfData.basis, stwfData.TX.shift(-1) < 2, color = 'r', alpha =0.3, edgecolors='none')
ax1.legend()
ax1.set_ylabel('TX ret% next 10 day(s)')
ax1.set_xlabel('short <--basis call--> long')

ax2.grid(True)
ax2.scatter(stwfData.basis, stwfData.TX.shift(-1) < -2, color = 'r', alpha =0.05, edgecolors='none')
ax2.legend()
ax2.set_ylabel('TX ret% next 10 day(s)')
ax2.set_xlabel('short <--basis call--> long')

ax3.grid(True)
ax3.scatter(stwfData.basis, stwfData.TX.shift(-1), color = 'b', alpha =0.3, edgecolors='none')
ax3.legend()
ax3.set_ylabel('TX ret% next 10 day(s)')
ax3.set_xlabel('short <--basis call--> long')

ax4.grid(True)
ax4.scatter(stwfData.basis, stwfData.TX.shift(-1), color = 'b', alpha =0.05, edgecolors='none')
ax4.legend()
ax4.set_ylabel('TX ret% next 10 day(s)')
ax4.set_xlabel('short <--basis call--> long')

