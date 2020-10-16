# POA

This is a classic padding oracle attack. However, the padding scheme is ISO/IEC 7816-4 instead of PKCS\#7. In ISO/IEC 7816-4, we have the first byte of padding set to `80`, and the remaining set to `00` until the end of the block is reached.

Different from PKCS\#7, we cannot know how many bytes are padded directly from guessing the last byte, since we are not sure whether the last byte is `00` or `80` (they all return success from the server).

Therefore, my idea is to first discover the number of paddings, then start bruteforce the plaintext byte-by-byte using the classic padding oracle attack.

The way to discover the number of paddings are as follows. First, we know that the given ciphertext contains a valid padding, which means the plaintext should be in "`xxxxxxxxxxx\x80\x00\x00\x00...`" format. 

The trick here is to use xor operation. If we original byte is `\x00`, we could xor it with `\x80`, and send if the modified ciphertext (it is decrypted as `xxxxxxxxxxx\x80\x00\x00\x00...\x80`) is valid or not. In this case we will get a valid response, since we can see can find `\x80` from the end and no bytes other than `\x00` and `\x80` are found.

We can keep trying byte-by-byte, the procedure should look like below.
1. `xxxxxxxxxxx\x80\x00\x00\x00\x80` (valid)
2. `xxxxxxxxxxx\x80\x00\x00\x80\x00` (valid)
3. `xxxxxxxxxxx\x80\x00\x80\x00\x00` (valid)
4. `xxxxxxxxxxx\x80\x80\x00\x00\x00` (valid)
5. `xxxxxxxxxxx\x00\x00\x00\x00\x00` (**invalid**)

The reason why step 5 is invalid is because we cannot find the byte `\x80` that represents the end of the padding. Therefore, we can find the padding length according to this procedure.

After we find the padding length, we can modify the last byte and the byte after the last byte (it means take one "x" and the last "\x80" in the example above). Modify that "\x80" to "\x00" and bruteforce which byte makes the decryption to be valid (it could only be `\x80` to be deemed as valid, since we do not have any `\x80` after that). Continue this procedure, we would get the plaintext at last.

The script to solve this challenge is located at [solve.py](./solve.py)
