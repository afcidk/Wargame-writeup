# 2018-rev

I don't think my solution is the intended solution....
I just set argc=2018, argv[0][0]=1, and envp[0][0]=1 as suggested, then the binary asked me to change my date and timezone. I changed them then passed the level :b.

`sudo timedatectl set-timezone UTC`
`sudo date -s "2018/01/01 00:00:00"`
`python3 solve.py`

Remember to turn off automatic date & time and automatic timezone if needed!
