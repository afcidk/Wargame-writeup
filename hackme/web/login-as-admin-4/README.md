查看原始碼，可以發現輸入 user 等於 "admin" 時，會被重新導向到 `./failed=1`

在使用 header('Location: xxx') 之後，我們應該要使用 exit() 來結束這個 script, 否則這個頁面會繼續往下執行，執行完再被重新導向。

因為題目沒有在重新導向後加上 `exit()`, 所以我們可以使用 `cURL` 之類的工具來避免


payload: `curl --data "name=admin&password=pass" "https://hackme.inndy.tw/login4/"`
