#!/usr/bin/python3
import hashlib

firstname = 'susan'
firstname_backwards = firstname[::-1]
hash = 'abeb6f8eb5722b8ca3b45f6f72a0cf17c7028d62a15a30199347d9d74f39023f'

for i in range(1, 1000000001):
    pwd = f"{firstname}_{firstname_backwards}_{i}"
    hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest()
    print(pwd, ":", hashed_pwd, end="\r")
    if hashed_pwd == hash:
        print(pwd)
        break
