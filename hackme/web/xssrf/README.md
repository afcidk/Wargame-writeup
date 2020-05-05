## Flag 1
1. Found backup.zip using fuzzer
2. Tried using pkcrack to unzip the encrypted zip file (if pkcrack shows that plaintext is longer that ciphertext, you could try different compression speed (see `-#` in `man zip`)
3. Nothing intersting in the decrypted zip file

1. The admin says that it reads all mail, so we can try insert a stored-xss payload in the mail to the admin.
2. The payload for xssme is in `input.txt`. I encode it to bypass the restriction from the server.
3. We could steal the cookie from the admin and find the first flag.
```
PHPSESSID=3bccn0copaud26tj5umlha0453; FLAG_XSSME=FLAG{Sometimes, XSS can be critical vulnerability <script>alert(1)</script>}; FLAG_2=IN_THE_REDIS
```

## Flag 2
1. We could find another interesting entry `request.php` from admin's perspective.
2. It seems there's ssrf vulnerability in this web page.
3. We could first try `url=file:///etc/passwd` to see if we could read the content.
4. Looks good! We could try to read `config.php` as suggested in `https://xssrf.hackme.inndy.tw/robots.txt`.
5. Got the second flag, the payload for Flag 2 is in `input2.txt`. You could encode it by modifing `encode.py`.
```
FLAG{curl -v -o flag --next flag://in-the.redis/the?port=25566&good=luck}
```
