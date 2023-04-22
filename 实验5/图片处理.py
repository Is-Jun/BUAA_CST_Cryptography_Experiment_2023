def Sbox(A):  # 非线性变换t 输入32位整数A 输出32位整数B
    S_box = [[0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05],
             [0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99],
             [0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62],
             [0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6],
             [0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8],
             [0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35],
             [0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87],
             [0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e],
             [0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1],
             [0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3],
             [0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f],
             [0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51],
             [0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8],
             [0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0],
             [0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84],
             [0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48]]
    B = (S_box[((A & 0xff000000) >> 24) // 16][((A & 0xff000000) >> 24) % 16] << 24) \
        + (S_box[((A & 0xff0000) >> 16) // 16][((A & 0xff0000) >> 16) % 16] << 16) \
        + (S_box[((A & 0xff00) >> 8) // 16][((A & 0xff00) >> 8) % 16] << 8) \
        + S_box[(A & 0xff) // 16][(A & 0xff) % 16]
    return B


def L(B):  # 线性变换L 输入32位整数B 输出32位整数C
    C = B ^ (((B << 2) & 0xffffffff) + (B >> 30)) ^ (((B << 10) & 0xffffffff) + (B >> 22)) \
        ^ (((B << 18) & 0xffffffff) + (B >> 14)) ^ (((B << 24) & 0xffffffff) + (B >> 8))
    return C


def T(X1, X2, X3, rk):  # 合成置换T 输入均为32位整数 输出32位整数
    return L(Sbox(X1 ^ X2 ^ X3 ^ rk))


def F(X0, X1, X2, X3, rk):  # 轮函数F
    return X0 ^ T(X1, X2, X3, rk)


def L_(B):  # 秘钥拓展线性变换L' 输入32位整数B 输出32位整数
    return B ^ (((B << 13) & 0xffffffff) + (B >> 19)) ^ (((B << 23) & 0xffffffff) + (B >> 9))


def T_(K1, K2, K3, CK):
    return L_(Sbox(K1 ^ K2 ^ K3 ^ CK))


def F_(K0, K1, K2, K3, CK):
    return K0 ^ T_(K1, K2, K3, CK)


def generate_key(MK):  # MK初始秘钥 以4*32bit列表传入
    key = []
    K = [0] * 36
    FK = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc]
    CK = [0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,
          0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
          0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
          0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
          0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
          0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
          0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
          0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279]
    for i in range(4):  # K的初始化
        K[i] = FK[i] ^ MK[i]
    for i in range(32):
        K[i + 4] = F_(K[i], K[i + 1], K[i + 2], K[i + 3], CK[i])
        key.append(K[i + 4])
    return key


def SM4(s, key):  # s以128bit字符串传入
    X = [0] * 4
    for i in range(4):
        X[i] = int(s[0 + 8 * i:8 * (i + 1)], base=16)
    for i in range(32):
        _ = F(X[0], X[1], X[2], X[3], key[i])
        X = X[1:]
        X.append(_)
    X = X[::-1]
    return (X[0] << 96) ^ (X[1] << 64) ^ (X[2] << 32) ^ X[3]


def ECB(s, key):  # s为任意长的字符串，去除0x
    text = []
    result = ''
    for i in range(0, len(s) - 32, 32):  # 32*4=128bit 为SM4输入长度
        text.append(s[i:32 + i])
    if len(s) % 32 == 0:
        text.append(s[len(s) - 32:])
    else:
        _ = (32 - len(s) % 32) // 2
        text.append(s[len(s) - len(s) % 32:] + hex(_)[2:].zfill(2) * _)
    for item in text[:-1]:
        X = SM4(item, key)
        _ = hex(X)[2:].zfill(32)
        result += _
    X = SM4(text[-1], key)
    _ = hex(X)[2:].zfill(32)
    if len(s) % 32 == 0:
        result += _
    else:
        result += _[:len(s) % 32]
    return result


def CBC(s, IV, key):  # s为任意长的字符串，去除0x  IV为整数
    text = []
    result = ''
    for i in range(0, len(s) - 32, 32):  # 32*4=128bit 为SM4输入长度
        text.append(s[i:32 + i])
    if len(s) % 32 == 0:
        text.append(s[len(s) - 32:])
    else:
        _ = (32 - len(s) % 32) // 2
        text.append(s[len(s) - len(s) % 32:] + hex(_)[2:].zfill(2) * _)
    for item in text[:-1]:
        IV ^= int(item, base=16)
        X = SM4(hex(IV)[2:].zfill(32), key)
        IV = X
        _ = hex(IV)[2:].zfill(32)
        result += _
    IV ^= int(text[-1], base=16)
    X = SM4(hex(IV)[2:].zfill(32), key)
    _ = hex(X)[2:].zfill(32)
    if len(s) % 32 == 0:
        result += _
    else:
        result += _[:len(s) % 32]
    return result


def input_bmp(filename):
    head = b''
    s = ''
    count = 0
    with open(filename, 'rb') as f:
        while True:
            byte = f.read(1)
            if byte == b'':
                break
            if count < 54:
                head += byte
            else:
                s += '%02x' % int.from_bytes(byte, byteorder='big')
            count += 1
    return head, s


def output_bmp(head, s, filename):
    with open(filename, 'wb') as f:
        f.write(head)
        for i in range(0, len(s), 2):
            byte = int(s[i:i + 2], base=16).to_bytes(1, byteorder='big')
            f.write(byte)


def main():
    k = "0x00112233445566778899aabbccddeeff"
    IV = 0x000102030405060708090a0b0c0d0e0f
    MK = [0] * 4
    for i in range(4):
        MK[i] = int(k[2 + 8 * i:10 + 8 * i], base=16)
    key = generate_key(MK)
    head, s = input_bmp('submit.bmp')
    s_ECB = ECB(s, key)
    s_CBC = CBC(s, IV, key)
    output_bmp(head, s_ECB, 'ECB.bmp')
    output_bmp(head, s_CBC, 'CBC.bmp')


if __name__ == '__main__':
    main()