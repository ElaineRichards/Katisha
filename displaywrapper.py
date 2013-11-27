#!/usr/bin/env python
# This is a simple wrapper so that outputs can be displayed on a web page.
# Super simple
def wrapoutput(stringtoprint):
    print ("Content-type: text/html\n\n<html><body><pre>")
    print stringtoprint
    print ("</pre></body></html>")
    return

version = "1.0"