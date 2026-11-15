#!/usr/bin/env python3
import re
import sys


def parse_leaks(data):
    toks = re.findall(rb"0x([0-9a-fA-F]{1,16})\b", data)
    return [int(t, 16) for t in toks]


def slots_to_memory(slots, word=8):
    return b"".join(v.to_bytes(word, "little") for v in slots)


def printable_strings(blob, minlen=4):
    return re.findall(rb"[ -~]{%d,}" % minlen, blob)


def find_flag(blob, patterns=(rb"\w+\{[^}]+\}", rb"FLAG=[ -~]+")):
    for pat in patterns:
        m = re.search(pat, blob)
        if m:
            return m.group().split(b"\x00", 1)[0]
    return None


def recover(data):
    slots = parse_leaks(data)
    blob = slots_to_memory(slots)
    return slots, blob


def main():
    if len(sys.argv) > 1:
        data = open(sys.argv[1], "rb").read()
    else:
        data = sys.stdin.buffer.read()

    slots, blob = recover(data)
    print(f"[+] слотов разобрано: {len(slots)}")
    print(f"[+] восстановлено байт: {len(blob)}\n")

    print("=== печатаемые строки ===")
    for s in printable_strings(blob, minlen=4):
        print("   ", s.decode(errors="replace"))

    flag = find_flag(blob)
    print("\n=== флаг ===")
    print("   ", flag.decode(errors="replace") if flag else "не найден")


if __name__ == "__main__":
    main()
