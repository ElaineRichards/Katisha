#!/usr/bin/env python
import urllib 
import re
#import sys 
import fileinput


def get_quote(symbol):
    returnvalue = 0
    url = "http://finance.yahoo.com/q?s=" + symbol + "&ql=1" 
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    # This part can change if yahoo changes their html markup in the page. This
    # grabs <span id= etc > the price</span>
    regex = '<span id="yfs_' + '(...)_'+symbol+'">(.+?)</span>'
    pattern = re.search(regex,htmltext)
    if ( pattern.group(0) ):
        returnvalue= pattern.group(0)
    #This strips the <stuff> out of the line, leaving just the number
    splitline= re.split("<(.+?)>",returnvalue)
    if (splitline):
        if (splitline[2]):
            returnvalue=splitline[2]
    
    return float(returnvalue)

runningtotal = 0

stockfile = open('stocknumberfile','r')
for line in stockfile:
    numberofshares = 0
    value = 0
    total = 0
    [thestock, n] = re.split(":",line)
    try:
         numberofshares = float(n)
    except:
         print "could not convert n to float",
         print n
    
    if (thestock):
        try:
            value = get_quote(thestock) 
        except:
            print "Couldn't find price for %s" % thestock
    try:
        total = numberofshares * float(value)
    except:
        print "Can't multiply "
    try:
        print "%s: %.2f : %d : %.2f "% (thestock,value,numberofshares,total)
    except:
         print "could not print fussy line"
    runningtotal = runningtotal + total

stockfile.close

print "Complete total is : %d" % runningtotal
