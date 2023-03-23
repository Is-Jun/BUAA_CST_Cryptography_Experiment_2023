def vernam_cipher(k, s, way):
    if way == 1:
        cipher = ''
        for i in range(len(s)):
            cipher += chr(ord(s[i]) ^ ord(k[i % len(k)]))
        return cipher
    else:
        plaintext = ''
        for i in range(len(s)):
            plaintext += chr(ord(s[i]) ^ ord(k[i % len(k)]))
        return plaintext


k = input().strip()
s = input().strip()
way = int(input())

print(vernam_cipher(k, s, way))