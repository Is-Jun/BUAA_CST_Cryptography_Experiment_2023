from hashlib import sha1
from random import randint


def construct_the_message(file_name1, file_name2, max=100):
    with open(file_name1, 'r') as f1, open(file_name2, 'w') as f2:
        temp = ' ' + chr(8)  # 或者' ' + chr(8) + ' '
        while True:
            m = f1.readline().strip()
            if not m:
                break
            f2.write(m + '\n')
            m_list = m.split(' ')
            l = len(m_list)
            loop = randint(1, max)
            for i in range(loop):
                r = temp * randint(0, max)
                for i in range(l):
                    r += (m_list[i] + temp * randint(1, max))
                f2.write(r + '\n')


construct_the_message('CorrectMessage.txt', 'correct_message.txt', 4500)
construct_the_message('WrongMessage.txt', 'wrong_message.txt', 4500)


def SHA1_attack_2():
    """
    只要求至少前32bit相同则需构造2^16个消息，保证产生碰撞的概率大于0.5
    """
    correct_hash = []
    correct_msg = []
    worry_msg = []
    with open('correct_message.txt', 'r') as f1, open('wrong_message.txt', 'r') as f2:
        while True:
            m = f1.readline().strip()
            if not m:
                break
            correct_msg.append(m)
            correct_hash.append(sha1(m.encode('utf-8')).hexdigest()[:8])
        print(len(correct_hash))
        while True:
            if len(worry_msg) == 3:
                break
            m = f2.readline().strip()
            if not m:
                print('failed >_<')
                break
            judge = sha1(m.encode('utf-8')).hexdigest()[:8]
            if judge in correct_hash:
                worry_msg.append([correct_msg[correct_hash.index(judge)], m])
    return worry_msg


def main():
    wor_msg = SHA1_attack_2()
    # print(len(wor_msg))
    # with open('submit.txt', 'w') as f:
    #     for i in range(len(wor_msg)):
            # f.write(wor_msg[i][0] + '\n')
            # f.write(wor_msg[i][1] + '\n')
            # print(sha1(wor_msg[i][0].encode('utf-8')).hexdigest())
            # print(sha1(wor_msg[i][1].encode('utf-8')).hexdigest())

    for i in range(len(wor_msg)):
        print(wor_msg[i][0])
        print(wor_msg[i][1])
        print(sha1(wor_msg[i][0].encode('utf-8')).hexdigest())
        print(sha1(wor_msg[i][1].encode('utf-8')).hexdigest())


if __name__ == '__main__':
    main()