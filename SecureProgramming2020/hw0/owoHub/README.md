# owoHub
We can see the source code entry from the given web page (https://owohub.zoolab.org/source)

### Source code
```javascript=
const express = require("express");
const http = require("http");
const { FLAG, cuteOnlyImages } = require("./secret");

const app = express();

app.get('/', (_, response) => {
    response.sendFile(__dirname + "/index.html");
});
app.get("/source", (_, res) => {
    res.sendFile(__filename);
});
app.get('/auth', (request, response) => {
    const { username, cute } = request.query;

    if (typeof username !== "string" || typeof cute !== "string" ||
        username === "" || !cute.match("(true|false)$")) {
        response.send({ error: "Whaaaat owo?" });
        return;
    }

    if (username.match(/[^a-z0-9]+/i)) {
        response.send({ error: "`Username` should contain only letters & numbers, owo." });
        return;
    }

    const userInfo = `{"username":"${username}","admin":false,"cute":${cute}}`;

    const api = `http://127.0.0.1:9487/?data=${userInfo}&givemeflag=no`;
    http.get(api, resp => {
        resp.setEncoding("utf-8");
        if (resp.statusCode === 200)
            resp.on('data', data => response.send(data));
        else
            response.send({ error:  "qwq..." });
    });
})
app.listen(8787, "0.0.0.0");

// Internal server, can't directly access by external users.
const authServer = express();
authServer.get("/", (request, response) => {
    const { data, givemeflag } = request.query;
    const userInfo = JSON.parse(data);
    if (givemeflag === "yes" && userInfo.admin) // You don't need to be cute to get the flag ouo!
        response.send(FLAG);
    else
        response.send({
            username: `Hellowo, ${userInfo.username}${userInfo.admin ? "<(_ _)>" : ""}!`,
            imageLinks: cuteOnlyImages.map(link => userInfo.cute ? link : "javascript:alert('u are not cute oAo!')")
        });
});
authServer.listen(9487, "127.0.0.1");
```

The server opens 8787 port which could be accessed by anyone, and 9487 port restricted to localhost.

The key to this challenge is at line 45, we need to fulfill two prequisites to get the flag.
```javascript=
if (givemeflag === "yes" && userInfo.admin)
    response.send(FLAG);
```

### Make `userInfo.admin` to `true`
At line 27, `userInfo.admin` is assigned to false, which seemes to be unchangable. However, the user input is not sanitized, and is passed directly to another request in line 29.

The request template is as follows
```
{"username":"${username}","admin":false,"cute":${cute}}
```

We can overlap `admin` to `true` after the `cute` key. At this point we can make the request URL to:
```
https://owohub.zoolab.org/auth?
username=abc&cute=true,"admin":true
```
Response:
```
{"username":"Hellowo, abc<(_ _)>!","......."
```
According to line 49, we can verify that we really changed `admin` to `true`!

### Make givemeflag equal to "yes"
The request to the local api server is 
```javascript
const userInfo = `{"username":"${username}","admin":false,"cute":${cute}}`;
const api = `http://127.0.0.1:9487/?data=${userInfo}&givemeflag=no`;
```
The previous trick may not work now, since we don't have user controllable field after `givemeflag=no`

However, we still can take advantage of unsanitized `userInfo`.

The idea is that we could forge `userInfo` to end earlier (using `}`), and let the remaining string as url fragments (using `#`).

Also, there exists a filter at line 17 checking if cute has a `true` or `false` suffix (`cute.match("(true|false)$"`).

The request: `https://owohub.zoolab.org/auth?username=abc&cute=true,"admin":true}&givemeflag=yes#true`

The response: `{"error":"Whaaaat owo?"}`

There is still a simple problem. We need the payload to be regarded as value of `cute` key, so we have to encode `&` and `#` in our request.

Therefore, the request should be
```
https://owohub.zoolab.org/auth?
username=abc&cute=true,"admin":true}
%26givemeflag=yes%23true
```

Flag:
`FLAG{owo_ch1wawa_15_th3_b35t_uwu!!!}`

