一開始直接用 foremost 看看裏面有沒有藏東西
```
├── audit.txt
├── png
│   └── 00000000.png
└── zip
    └── 00000094.zip
```

發現裏面還有一個壓縮檔，試著解開看看
![](https://i.imgur.com/3OtQNCb.png)

發現要密碼，而且 flag 似乎就在裏面。
另外，發現裏面還有另外一個 png 圖檔，猜測可能是加密過的原圖。

使用 `pkcrack` 工具來試試看
* 先把壓縮原本的圖片 (zip)
    `zip zipped.zip 00000000.png`
* 用 `pkcrack` 進行 plaintext attack
    ```
    pkcrack -P png/zipped.zip -p 00000000.png -C zip/00000094.zip -c meow/t39.1997-6/p296x100/10173502_279586372215628_1950740854_n.png -d decrypted.zip -a
    ```

成功了，最後再解壓縮得到的 `decrypted.zip`，查看裡面的 `flag`，得到 flag。
