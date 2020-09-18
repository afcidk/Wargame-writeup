from PIL import Image

names = [
    "00000206.jpg", "00000299.jpg", "00000308.jpg", "00000311.jpg",
    "00000315.jpg", "00000330.jpg", "00000341.jpg", "00000346.jpg",
    "00000359.jpg", "00000218.jpg", "00000229.jpg", "00000238.jpg",
    "00000256.jpg", "00000266.jpg", "00000277.jpg", "00000288.jpg"
]

arr2 = []
for n in names:
    im = Image.open(n)
    px = im.load()
    arr2.append(px[66, 99][0])

arr = [
    250, 241, 107, 182, 244, 110, 21, 129, 17, 240, 155, 200, 111, 111, 225,
    110, 180, 224, 156, 194, 29, 106, 141, 216, 99, 58, 59, 191, 45, 227, 184,
    221, 63, 139, 223, 232, 129, 201, 121, 62, 164, 113, 247, 230, 67, 108,
    182, 231
]

arr3 = [0 for i in range(256)]
arr4 = [0 for i in range(256)]
arr5 = [0 for i in range(len(arr))]

for j in range(256):
    arr3[j] = arr2[j % len(arr2)]
    arr4[j] = j

num = j = 0
for j in range(256):
    num = (num + arr4[j] + arr3[j]) % 256
    num2 = arr4[j]
    arr4[j] = arr4[num]
    arr4[num] = num2

num3 = 0
num = 0
j = 0
for j in range(len(arr)):
    num3 += 1
    num3 %= 256
    num += arr4[num3]
    num %= 256
    num2 = arr4[num3]
    arr4[num3] = arr4[num]
    arr4[num] = num2
    num4 = arr4[(arr4[num3] + arr4[num]) % 256]
    arr5[j] = (arr[j] ^ num4) & 0xff

for a in arr5:
    print(chr(a), end='')
