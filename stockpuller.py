#!/usr/bin/env python
#
# The inputs for this app are stored in a file called stocknumberfile, which is not uploaded into Git. I have my copy
# locally and no one needs to know my holdings but me.
#
# The format for stocknumberfile is that each line has the stock symbol, a colon, and the number of shares.
# ex.
#    goog:10
#    msft:20
#import displaywrapper
import sys
sys.path.append(".")
import displaywrapper
import urllib 
import re
#import sys 
import fileinput


def get_quote_from_yahoo(symbol):
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

outputline = ""
stockfile = open('stocknumberfile','r')
for line in stockfile:
    numberofshares = 0
    value = 0
    total = 0
    [thestock, n] = re.split(":",line)
    try:
         numberofshares = float(n)
    except:
         outputline +=  "could not convert n to float",
         outputline += str(n)
    
    if (thestock):
        try:
            value = get_quote_from_yahoo(thestock) 
        except:
            outputline += "Couldn't find price for %s" % thestock
    try:
        total = numberofshares * float(value)
    except:
        outputline += "Can't multiply "
    try:
        outputline += "%s: %.2f : %d : %.2f "% (thestock,value,numberofshares,total)
    except:
         outputline += "could not print fussy line"
    runningtotal = runningtotal + total

stockfile.close
outputline += "Complete total is : %d" % runningtotal

displaywrapper.wrapoutput( outputline )
                          
