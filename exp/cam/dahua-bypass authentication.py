import argparse
import socket
import struct
import sys

top_parser = argparse.ArgumentParser(description='Login using admin:01testit and get the software version')
top_parser.add_argument('-i', '--ip', action="store", dest="ip", required=True, help="The IPv4 address to connect to")
top_parser.add_argument('-p', '--port', action="store", dest="port", type=int, help="The port to connect to", default="37777")
args = top_parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "[+] Attempting connection to " + args.ip + ":" + str(args.port)
sock.connect((args.ip, args.port))
print "[+] Connected!"

login = ("\xa0\x00\x00\x60\x00\x00\x00\x00" + 
         "\xc4\xa3\xaf\x48\x99\x56\xb6\xb4" + # username hash
         "\x7e\x48\xc4\x86\x90\x98\x54\xf3" + # password hash
         "\x05\x02\x00\x01\x00\x00\xa1\xaa")
sock.sendall(login)
resp = sock.recv(1024)

if len(resp) != 32:
    print 'What is this?'
    sys.exit(0)

session_id_bin = resp[16:20]

session_id_int = struct.unpack_from('I', session_id_bin)
if session_id_int[0] == 0:
	print "Failed to log in. Response:"
	print resp
	sys.exit(0)

print str(session_id_int[0])

json = '{"id":1,"method":"magicBox.getSoftwareVersion","params":null,"session":' + str(session_id_int[0]) + '}\n\x00'
size = struct.pack("I", len(json))
json_request = "\xf6\x00\x00\x00" + size + '\x01\x00\x00\x00\x00\x00\x00\x00' + size + '\x00\x00\x00\x00' + session_id_bin + '\x00\x00\x00\x00' + json
sock.sendall(json_request)
print sock.recv(1024)

sock.close()