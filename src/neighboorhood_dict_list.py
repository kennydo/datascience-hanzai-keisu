# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import csv
from sets import Set

DATA_PATH = '/Users/Allen/Dropbox/CS194FinalProject/'

with open(DATA_PATH + 'ZillowSFExcel.csv', 'rU') as csvfile:
    zillowreader = csv.reader(csvfile, delimiter=',')
    
    dictsetter = []
    zillowreader.next()
    for row in zillowreader:
        dictsetter.append(row)

housingdict = {}        
for i in range(1, len(dictsetter)):
    housingdict[dictsetter[i][0]] = float(dictsetter[i][1])


DATA_PATH = '/Users/Allen/Dropbox/CS194FinalProject/'

with open(DATA_PATH + 'sfpd_incidents_2013_with_neighborhoods.csv', 'rU') as csvfile:
    neighborhoodreader = csv.reader(csvfile, delimiter=',')
    
    neighborhoodset = Set([])
    for row in neighborhoodreader:
        neighborhoodset.add(row[9])
        
neighborhoodset.remove('')        
neighborhoodlist = list(neighborhoodset)

#neighborhoodlist
#housingdict['Marina']
    

