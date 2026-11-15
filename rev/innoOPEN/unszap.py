import sys

f =  open(sys.argv[1], 'rb').read()
data = f[4:-8]
res = b''

for i in range (0, len(data), 2):
    count = data[i]
    byte = data[i + 1]
    res += bytes([byte]) * count

print(res.decode("utf-8"))
