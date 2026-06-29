from packer import build_glyp

entries = [
    ("manifest.mf",        b"lol=kek\n", 1),
    ("covers/cover.svg",   b":D",      2),
]

open("test.glyp", "wb").write(build_glyp(entries))
