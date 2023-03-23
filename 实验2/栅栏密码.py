def fence_cipher(k, s, way):
    list1 = list(s)
    if way == 1:
        list2 = []
        for i in range(k):
            for j in range(i, len(list1), k):
                list2.append(list1[j])
        list1 = list2
        return list1
    else:
        list2 = []
        num = len(list1) // k
        rec = len(list1) - num * k
        # print(len(list1))
        num += 1
        for i in range(0, num):
            for j in range(0, k):
                if j < rec:
                    list2.append(list1[j * num + i])
                else:
                    if (k - 1) * num + rec - (k - 1) + i >= len(list1):
                        break
                    list2.append(list1[j * num + rec - j + i])
        list1 = list2
        return list1


k = int(input())
s = input().strip()
way = int(input())

for i in fence_cipher(k, s, way):
    print(i, end='')