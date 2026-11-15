from pwn import *
from ctypes import CDLL
import time

NAMES = ['Joseph','Jessica','Thomas','Sarah','Charles','Karen','Christopher',
         'Nancy','Daniel','Lisa','Matthew','Margaret','Tom','Betty','Donald',
         'Sandra','Mark','Ashley','Paul','Jerry']
libc = CDLL("libc.so.6")

while True:
    libc.srand(int(time.time()))
    name = NAMES[libc.rand() % 20]
    io = remote("109.233.56.90", 11632)
    io.sendafter(b"name: ", name.encode() + b"\n")
    out = io.recvall(timeout=3)
    if b"{" in out:
        print(out.decode(errors="replace")); break
    io.close()
