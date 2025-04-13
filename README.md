# NO_ONX
NO_ONX is a lightweight tool but useful to analysis, investigattion, security monitoring for Linux System
## Requirement
- OS: Linux (Ubuntu, Debian)
- Python: 3.1x
- C++17 and C++ Compiler (`g++`)

## Installation
### Installing Python and C++ (Skip this if you have)
```bash
sudo apt update
sudo apt install python3 g++
```

### Install required libary
(Note: If you're using Kali Linux, you can skip this step)␣␣
For python:
```bash
pip install -r python_requirements.txt
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

python readfile.py - Read file content␣␣
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
