from hashlib import sha1
from math import ceil


def MGF(mgfSeed, maskLen):
    if len(mgfSeed) // 2 > 2 ** 61 - 4:
        return -1
    counter = 0
    hLen = 20
    restLen = maskLen
    mask = ''
    while restLen > 0:
        C = hex(counter)[2:].zfill(8)
        mask += sha1(bytearray.fromhex(mgfSeed + C)).hexdigest()
        counter += 1
        restLen -= hLen
    return mask[:maskLen * 2]


def sign(M:str, emBits, salt, d, n):
    emLen = ceil(emBits / 8)
    bc = 'bc'
    padding1 = '0' * 16
    padding2 = '00' * (emLen - sLen - hLen - 2) + '01'
    mHash = sha1(M.encode('utf-8')).hexdigest()
    M_ = padding1 + mHash + salt
    H = sha1(bytearray.fromhex(M_)).hexdigest()
    DB = padding2 + salt
    mgf_H = MGF(H, emLen - hLen - 1)
    maskedDB = hex(int(DB, 16) ^ int(mgf_H, 16))[2:].zfill((emLen - hLen - 1) * 2)
    EM = maskedDB + H + bc
    s = pow(int(EM, 16), d, n)
    return hex(s)[2:].zfill(n_bit // 4)


def vrfy(M:str, emBits, e, s, n):
    emLen = ceil(emBits / 8)
    padding1 = '0' * 16
    padding2 = '00' * (emLen - sLen - hLen - 2) + '01'
    mHash = sha1(M.encode('utf-8')).hexdigest()
    EM = hex(pow(int(s, 16), e, n))[2:].zfill(emLen * 2)
    if emLen < hLen + sLen + 2:
        return 'False'
    if EM[-2:] != 'bc':
        return 'False'
    maskedDB = EM[:(emLen - hLen - 1) * 2]
    H = EM[(emLen - hLen - 1) * 2:(emLen - 1) * 2]
    b = bin(int(maskedDB[:2], 16))[2:].zfill(8)
    if b[:8 * emLen - emBits] != '0' * (8 * emLen - emBits):
        return 'False'
    dbMask = MGF(H, emLen - hLen - 1)
    DB = hex(int(maskedDB, 16) ^ int(dbMask, 16))[2:].zfill((emLen - hLen - 1) * 2)
    b = bin(int(DB[:2], 16))[2:].zfill(8)
    b = '0' * (8 * emLen - emBits) + b[8 * emLen - emBits:]
    DB = hex(int(b, 2))[2:].zfill(2) + DB[2:]
    if DB[:(emLen - sLen - hLen - 1) * 2] != padding2:
        return 'False'
    salt = DB[-2 * sLen:]
    M_ = padding1 + mHash + salt
    H_ = sha1(bytearray.fromhex(M_)).hexdigest()
    if H == H_:
        return 'True'
    else:
        return 'False'
    # 事实上，交到OJ，在验签时，只需判断最后这一步就行（）


def main():
    global hLen, sLen, n_bit
    hLen = 20
    sLen = 20
    n_bit = 1024
    m = input().strip()
    n = int(input())
    emBits = int(input())
    mode = input().strip()
    if mode == 'Sign':
        d = int(input())
        salt = input().strip()
        print(sign(m, emBits, salt, d, n))
    else:
        e = int(input())
        s = input().strip()
        print(vrfy(m, emBits, e, s, n))


if __name__ == '__main__':
    main()
