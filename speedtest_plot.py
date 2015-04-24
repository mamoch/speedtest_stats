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
ax1 = fig.add_axes([0.13, 0.13, 0.68, 0.8])

ax1.plot(data[:, 0], data[:, 3], marker='.', label='down')
ax1.plot(data[:, 0], data[:, 4], marker='.', label='up')

autoDL = AutoDateLocator()
autoDF = AutoDateFormatter(autoDL)

ax1.xaxis.set_major_locator(autoDL)
ax1.xaxis.set_major_formatter(autoDF)

startTime = data[0, 0]
endTime = data[-1, 0]

##################################################
# statistics
down_mean = np.trapz(data[:, 3], data[:, 0])/(endTime - startTime)
up_mean = np.trapz(data[:, 4], data[:, 0])/(endTime - startTime)

down_max = np.max(data[:, 3])
up_max = np.max(data[:, 4])

down_min = np.min(data[:, 3])
up_min = np.min(data[:, 4])

plt.plot([startTime, endTime], [down_mean, down_mean], label=r'$\langle \Downarrow \rangle$')
plt.plot([startTime, endTime], [up_mean, up_mean], label=r'$\langle \Uparrow \rangle$')

plt.annotate( \
    r'$\langle \Downarrow \rangle=' + '{:.1f}'.format(down_mean) + r'\,\rm{Mbit/s}$' + '\n' + \
    r'$\Downarrow_{+}=' + '{:.1f}'.format(down_max) + r'\,\rm{Mbit/s}$' + '\n' + \
    r'$\Downarrow_{-}=' + '{:.1f}'.format(down_min) + r'\,\rm{Mbit/s}$' + '\n\n' + \
    r'$\langle \Uparrow \rangle=' + '{:.1f}'.format(up_mean) + r'\,\rm{Mbit/s}$' + '\n' + \
    r'$\Uparrow_{+}=' + '{:.1f}'.format(up_max) + r'\,\rm{Mbit/s}$' + '\n' + \
    r'$\Uparrow_{-}=' + '{:.1f}'.format(up_min) + r'\,\rm{Mbit/s}$', \
    (1.02, 0.66), xycoords='axes fraction', verticalalignment='top')
##################################################

fig.autofmt_xdate()
ax1.set_ylabel('speed (Mbit/s)')
ax1.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)

#ax2 = ax1.twinx()
#ax2.plot(data[:, 0], data[:, 2], color='r', marker='.', label='Latency')
#ax2.set_ylabel('latency (ms)')

plt.savefig('speedtest_stats.pdf')
plt.savefig('speedtest_stats.png', dpi=300)

plt.show()
