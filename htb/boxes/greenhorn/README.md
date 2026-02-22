## Port Scanning

```
sudo nmap -p 22,80,3000 -sV -sC -oA nmap/greenhorn-detailed 10.10.11.25
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-30 18:45 CEST
Nmap scan report for 10.10.11.25
Host is up (0.049s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 57:d6:92:8a:72:44:84:17:29:eb:5c:c9:63:6a:fe:fd (ECDSA)
|_  256 40:ea:17:b1:b6:c5:3f:42:56:67:4a:3c:ee:75:23:2f (ED25519)
80/tcp   open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://greenhorn.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
3000/tcp open  ppp?
| fingerprint-strings:
|   GenericLines, Help, RTSPRequest:
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest:
|     HTTP/1.0 200 OK
|     Cache-Control: max-age=0, private, must-revalidate, no-transform
|     Content-Type: text/html; charset=utf-8
|     Set-Cookie: i_like_gitea=84d6bcf0612af0b2; Path=/; HttpOnly; SameSite=Lax
|     Set-Cookie: _csrf=glOtBd96SGaFe4dybhy1n6uqmfw6MTcyNTAzNjMxODE5NjYxNjA1MA; Path=/; Max-Age=86400; HttpOnly; SameSite=Lax
|     X-Frame-Options: SAMEORIGIN
|     Date: Fri, 30 Aug 2024 16:45:18 GMT
|     <!DOCTYPE html>
|     <html lang="en-US" class="theme-auto">
|     <head>
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <title>GreenHorn</title>
|     <link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiR3JlZW5Ib3JuIiwic2hvcnRfbmFtZSI6IkdyZWVuSG9ybiIsInN0YXJ0X3VybCI6Imh0dHA6Ly9ncmVlbmhvcm4uaHRiOjMwMDAvIiwiaWNvbnMiOlt7InNyYyI6Imh0dHA6Ly9ncmVlbmhvcm4uaHRiOjMwMDAvYXNzZXRzL2ltZy9sb2dvLnBuZyIsInR5cGUiOiJpbWFnZS9wbmciLCJzaXplcyI6IjUxMng1MTIifSx7InNyYyI6Imh0dHA6Ly9ncmVlbmhvcm4uaHRiOjMwMDAvYX
|   HTTPOptions:
|     HTTP/1.0 405 Method Not Allowed
|     Allow: HEAD
|     Allow: HEAD
|     Allow: GET
|     Cache-Control: max-age=0, private, must-revalidate, no-transform
|     Set-Cookie: i_like_gitea=2520cd03f776d855; Path=/; HttpOnly; SameSite=Lax
|     Set-Cookie: _csrf=sn60_M7b5JvQsXGkPzXgB3s3QGk6MTcyNTAzNjMyMzUxOTc0NTY5NQ; Path=/; Max-Age=86400; HttpOnly; SameSite=Lax
|     X-Frame-Options: SAMEORIGIN
|     Date: Fri, 30 Aug 2024 16:45:23 GMT
|_    Content-Length: 0

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 96.23 seconds
```

---

## Port 80

Playing around with file bought us nothing.
gobuster gives us `/login.php` endpoint which reveal pluck's version(4.7.18)
This version is vulnerable and this POC works fine https://github.com/Rai2en/CVE-2023-50564_Pluck-v4.7.18_PoC
We need the password tho, which we can get on gitea
Just study the exploit, for whatever reason it doesn't work very well
Basically

1. create a php revshell
2. zip the revshell
3. listen on nc
4. login to pluck
5. go to /admin.php?action=managemodules
6. load the zip
7. go to /data/modules/revshell/revshell.php

---

## Port 3000

Go to "Explore" and check the repo.
Looks like `/login.php` is actually grabbing the password, hashing it with sha512 and checking it against `$ww` (imported from `/data/settings/pass.php`)
crackstation breaks the hash very easily

```
d5443aef1b64544f3685bf112f6c405218c573c7279a831b1fe9612e3a4d770486743c5580556c0d838b51749de15530f87fb793afdcc689b6b39024d7790163:iloveyou1
```

---

## User www-data

You can search around but will find nothing.
Just login to junior

```
junior:iloveyou1
```

---

## User junior

In home dir there's an openvas.pdf
Inside the .pdf there's a pixelized image containing a password

After some searching for unblurring/unpixelizing image/text-in-image, we find this tool https://github.com/spipm/Depix
Using the tool on the image reveals the root password

```
root:sidefromsidetheothersidesidefromsidetheotherside
```

---
