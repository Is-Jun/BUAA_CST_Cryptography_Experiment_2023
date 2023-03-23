def substitution_cipher(en_form, de_form, s, way):
    if way == 1: # encrypt
        cipher = ''
        for i in s:
            cipher += en_form[i]
        return cipher
    else:
        plaintext = ''
        for i in s:
            plaintext += de_form[i]
        return plaintext


t1 = input().strip()
t2 = input().strip()
s = input().strip()
way = int(input())
en_form = {}
de_form = {}
for i in range(26):
    en_form[t1[i]] = t2[i]
    de_form[t2[i]] = t1[i]

print(substitution_cipher(en_form, de_form, s, way))