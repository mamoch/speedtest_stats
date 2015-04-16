# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pylab as plt
from matplotlib.dates import strpdate2num, AutoDateLocator, AutoDateFormatter
import ConfigParser

cfgPars  = ConfigParser.RawConfigParser()
cfgPars.read('speedtest.cfg')

statsFile = cfgPars.get('Stats file', 'statsFile')

data = np.loadtxt(statsFile, delimiter='\t', usecols=(0, 5, 6, 7, 8), \
                  converters={0: strpdate2num('%Y-%m-%dT%H:%M:%S')})

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(data[:, 0], data[:, 3], marker='.', label='Download')
ax1.plot(data[:, 0], data[:, 4], marker='.', label='Upload')

autoDL = AutoDateLocator()
autoDF = AutoDateFormatter(autoDL)

ax1.xaxis.set_major_locator(autoDL)
ax1.xaxis.set_major_formatter(autoDF)

fig.autofmt_xdate()
ax1.set_ylabel('speed (Mbit/s)')
ax1.legend(loc=0)

#ax2 = ax1.twinx()
#ax2.plot(data[:, 0], data[:, 2], color='r', marker='.', label='Latency')
#ax2.set_ylabel('latency (ms)')

plt.savefig('speedtest_stats.pdf')

plt.show()
