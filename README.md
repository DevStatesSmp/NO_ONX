![have background](https://github.com/user-attachments/assets/0deb4708-e3a9-4219-85e4-3072af962c90)
(This is invincible title card, btw for fun)<br>

[CHANGELOG](https://github.com/DevStatesSmp/NO_ONX/blob/NO_ONX/CHANGELOG.md)

# NO_ONX
NO_ONX is a lightweight tool but useful to analysis, investigattion, security monitoring for Linux System
## Requirement
- OS: Linux (Ubuntu, Debian, Arch Linux)
- Python: 3.1x
- C++17 and C++ Compiler (`g++`)

## Installation
### Installing Python and C++ (Skip this if you have)<br>
For Ubuntu and Debian:
```bash
sudo apt update
sudo apt install python3 g++
```
<br>
For Arch Linux:
```bash
sudo pacman -Sy
sudo pacman -S python python-pip gcc base-devel openssl
```

### Install required libary
(Note: If you're using Kali Linux, you can skip this step)<br>
For python:
```bash
pip install -r python_requirements.txt
or if you using Arch:
sudo pacman -S python-psutil python-pyfiglet python-distro
```
and C++:
```bash
sudo apt install build-essential libssl-dev
```

## How to use
To view version and available command:

```bash
python noonx.py
```

Some example command you can use like:

python readfile.py - Read file content<br>
python detective.py - Monitor and detect suspecious activity on the system

Example:
```bash
┌──(USER㉿user)-[~/Desktop/no_onx]
└─$ python readfile.py                               
Ex: /home/-USER_NAME-/Desktop/example.txt
Please enter path of the file: 
/home/USER/Desktop/text.txt
Line 1: hello world!
Line 2: i love u :heart:
```

More commands and feature will be added in future, stay tuned!
