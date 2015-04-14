# -*- coding: utf-8 -*-

import speedtest_cli
from cStringIO import StringIO
import sys
import re
from datetime import datetime
import ConfigParser

cfgPars  = ConfigParser.RawConfigParser()
cfgPars.read('speedtest.cfg')

statsFile = cfgPars.get('Stats file', 'statsFile')

sysStdout_old = sys.stdout
sys.stdout = stringio = StringIO()

speedtest_cli.speedtest()
timestamp = datetime.now()

sys.stdout = sysStdout_old
output = stringio.getvalue()
del stringio

provider, IPv4 = re.findall('Testing from (.*) \(([0-9.]*)\)', output)[0]
hoster, hsLoc, hsDist, hsLaten = \
    re.findall('Hosted by (.*) \((.*)\) \[([0-9.]*) km\]: ([0-9.]*) ms', output)[0]
dlSpeed = re.findall('Download: ([0-9.]*) Mbit/s', output)[0]
upSpeed = re.findall('Upload: ([0-9.]*) Mbit/s', output)[0]

f = open(statsFile, 'a')

line = timestamp.strftime('%Y-%m-%dT%H:%M:%S') + '\t' + \
       provider + '\t' + \
       IPv4 + '\t' + \
       hoster + '\t' + \
       hsLoc + '\t' + \
       hsDist + '\t' + \
       hsLaten + '\t' + \
       dlSpeed + '\t' + \
       upSpeed + '\n'

f.write(line)
f.close()
