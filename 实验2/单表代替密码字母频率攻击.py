class get_out_of_loop(Exception):
    pass


def statistics(s):
    single = {chr(i + ord('a')): 0 for i in range(26)}
    double = {chr(i + ord('a')) + chr(j + ord('a')): 0 for i in range(26) for j in range(26)}
    triple = {chr(i + ord('a')) + chr(j + ord('a')) + chr(k + ord('a')): 0 for i in range(26) for j in
                        range(26) for k in range(26)}
    for i in range(len(s) - 2):  # 为了方便2/3阶统计，少个字母也没事（）
        single[s[i]] += 1
        double[s[i] + s[i+1]] += 1
        triple[s[i] + s[i+1] + s[i+2]] += 1
    single_frequency = sorted(single.items(), key=lambda x: x[1], reverse=True)
    double_frequency = sorted(double.items(), key=lambda x: x[1], reverse=True)
    triple_frequency = sorted(triple.items(), key=lambda x: x[1], reverse=True)
    return single_frequency, double_frequency, triple_frequency, single


def single_letter_predict(single_frequency):
    frequency_letter = ['e', 't', 'a', 'o', 'i', 'n',
                        's', 'r', 'h', 'l', 'd', 'c',
                        'u', 'm', 'f', 'p', 'g', 'w', 'y',
                        'b', 'v', 'k', 'x', 'j', 'q', 'z']
    form = [[] for i in range(26)]
    # 根据字母频率表，将密文对应的字母填入，因有多个字母频率相近
    # 故将所有可能性都填入列表中，后续进行选择排除
    form[ord(frequency_letter[0]) - ord('a')] = single_frequency[0][0]
    list_ = [1, 4, 9, 11, 20, 22, 26]
    for num in range(len(list_) - 1):
        for i in range(list_[num], list_[num + 1]):
            for j in range(list_[num], list_[num + 1]):
                form[ord(frequency_letter[j]) - ord('a')].append(single_frequency[i][0])
    return form


def remove(form, letter):
    for i in form:
        if type(i) == list:
            if letter in i:
                i.remove(letter)
                # if len(i) == 1:
                #     form[form.index(i)] = i[0]
    return form


def double_letter_predict(form, double_frequency):
    frequency_letters = ['th', 'he', 'in', 'er', 'an', 're',
                         'ed', 'on', 'es', 'st', 'en', 'at',
                         'to', 'nt', 'ha', 'nd', 'ou', 'ea',
                         'ng', 'as', 'or', 'ti', 'is', 'et',
                         'it', 'ar', 'te', 'se', 'hi', 'of']
    # th频率最高直接判断
    form[ord('t') - ord('a')] = double_frequency[0][0][0]
    form[ord('h') - ord('a')] = double_frequency[0][0][1]
    form = remove(form, double_frequency[0][0][0])
    form = remove(form, double_frequency[0][0][1])
    # 由e可确定r
    try:
        for i in range(10):
            for j in range(i + 1, 10):
                if double_frequency[i][0] == double_frequency[j][0][::-1]:
                    if form[ord('e') - ord('a')] != double_frequency[i][0][0]:
                        form[ord('r') - ord('a')] = double_frequency[i][0][0]
                        form = remove(form, double_frequency[i][0][0])
                    else:
                        form[ord('r') - ord('a')] = double_frequency[i][0][1]
                        form = remove(form, double_frequency[i][0][1])
                    raise get_out_of_loop()
    except get_out_of_loop:
        pass

    # 判断n，进而判断出i,a,o
    try:
        for i in range(15):
            for j in range(i + 1, 15):
                for k in range(j + 1, 15):
                    for l in range(k + 1, 15):  # in en an on
                        if double_frequency[i][0][1] == double_frequency[j][0][1] == \
                           double_frequency[k][0][1] == double_frequency[l][0][1]:
                            form[ord('n') - ord('a')] = double_frequency[i][0][1]  # 判断出n
                            form = remove(form, double_frequency[i][0][1])
                            list_ = [i, j, k, l]
                            for x in list_:  # 移除e
                                if double_frequency[x][0][0] == form[ord('e') - ord('a')]:
                                    list_.remove(x)
                                    break
                            for x in list_:  # 判断出i  a,o 在 {a,t,o} 组中，故可分出i
                                if double_frequency[x][0][0] in form[ord('i') - ord('a')]:
                                    form[ord('i') - ord('a')] = double_frequency[x][0][0]
                                    form = remove(form, double_frequency[x][0][0])
                                    list_.remove(x)
                                    break
                            for x in range(25):  # 通过ha判断出a,o
                                if double_frequency[x][0][0] == form[ord('h') - ord('a')]:
                                    if double_frequency[x][0][1] == double_frequency[list_[0]][0][0]:
                                        form[ord('a') - ord('a')] = double_frequency[list_[0]][0][0]
                                        form[ord('o') - ord('a')] = double_frequency[list_[1]][0][0]
                                        form = remove(form, double_frequency[list_[0]][0][0])
                                        form = remove(form, double_frequency[list_[1]][0][0])
                                        break
                                    elif double_frequency[x][0][1] == double_frequency[list_[1]][0][0] :
                                        form[ord('a') - ord('a')] = double_frequency[list_[1]][0][0]
                                        form[ord('o') - ord('a')] = double_frequency[list_[0]][0][0]
                                        form = remove(form, double_frequency[list_[0]][0][0])
                                        form = remove(form, double_frequency[list_[1]][0][0])
                                        break
                            raise get_out_of_loop()
    except get_out_of_loop:
        pass

    # 删除无用双字母后 frequency_letters = ['ed', 'es', 'st', 'nd', 'ou', 'ng', 'as', 'is', 'se']
    # 判断s 由st判断
    for i in range(30):
        if double_frequency[i][0][1] == form[ord('t') - ord('a')]:
            if double_frequency[i][0][0] not in form:
                form[ord('s') - ord('a')] = double_frequency[i][0][0]
                form = remove(form, double_frequency[i][0][0])
                break

    # frequency_letters = ['ed', 'nd', 'ou', 'ng']
    # 判断d 由ed判断，dl在同一频段所以可以大体猜测出l
    for i in range(30):
        if double_frequency[i][0][0] == form[ord('e') - ord('a')]:
            if double_frequency[i][0][1] not in form:
                form[ord('d') - ord('a')] = double_frequency[i][0][1]
                form = remove(form, double_frequency[i][0][1])
                break
    return form


def triple_letter_predict(form, triple_frequency):
    # 根据三字母判断
    # 剩下未确定的字母为 {b,c,f,g,j,k,l,m,p,q,u,v,w,x,y,z}
    # 根据our 判断u
    for i in triple_frequency:
        if i[0][0] + i[0][2] == form[ord('o') - ord('a')] + form[ord('r') - ord('a')]:
            if i[0][1] not in form:
                form[ord('u') - ord('a')] = i[0][1]
                form = remove(form, i[0][1])
                break

    # 根据ing 判断g
    for i in triple_frequency:
        if i[0][:2] == form[ord('i') - ord('a')] + form[ord('n') - ord('a')]:
            if i[0][2] not in form:
                form[ord('g') - ord('a')] = i[0][2]
                form = remove(form, i[0][2])
                break

    # 根据for 判断f
    for i in triple_frequency:
        if i[0][1:] == form[ord('o') - ord('a')] + form[ord('r') - ord('a')]:
            if i[0][0] not in form:
                form[ord('f') - ord('a')] = i[0][0]
                form = remove(form, i[0][0])
                break

    # 根据was 判断w
    for i in triple_frequency:
        if i[0][1:] == form[ord('a') - ord('a')] + form[ord('s') - ord('a')]:
            if i[0][0] not in form:
                form[ord('w') - ord('a')] = i[0][0]
                form = remove(form, i[0][0])
                break

    # 根据ver 判断v，vk在同一频段所以可以大体猜测出k
    for i in triple_frequency:
        if i[0][1:] == form[ord('e') - ord('a')] + form[ord('r') - ord('a')]:
            if i[0][0] not in form:
                form[ord('v') - ord('a')] = i[0][0]
                form = remove(form, i[0][0])
                break

    # 根据but 判断b
    for i in triple_frequency:
        if i[0][1:] == form[ord('u') - ord('a')] + form[ord('t') - ord('a')]:
            if i[0][0] not in form:
                form[ord('b') - ord('a')] = i[0][0]
                form = remove(form, i[0][0])
                break

    # 根据why 判断y
    for i in triple_frequency:
        if i[0][0:2] == form[ord('w') - ord('a')] + form[ord('h') - ord('a')]:
            if i[0][2] not in form:
                form[ord('y') - ord('a')] = i[0][2]
                form = remove(form, i[0][2])
                break

    # 剩下未确定字母 c,j,k,l,m,p,q,x,z
    # 根据pre概率最高判断出p
    for i in triple_frequency:
        if i[0][1:] == form[ord('r') - ord('a')] + form[ord('e') - ord('a')]:
            if i[0][0] not in form:
                form[ord('p') - ord('a')] = i[0][0]
                form = remove(form, i[0][0])
                break

    return form


def frequency_guess(form, triple_frequency):
    rank = []  # 用于最后排序 c,j,k,l,m,q,x,z
    for i in range(16):
        rank.append([0] * 9)
    # 验证l,k是否猜测正确
    # all 验证l
    for i in triple_frequency:
        if i[0][0] == form[ord('a') - ord('a')] and i[0][1] == i[0][2]:
            if i[0][1] == form[ord('l') - ord('a')][0]:
                rank[0][3] = i[0][1]
                break

    # ake 验证k
    for i in triple_frequency:
        if i[0][0] + i[0][2] == form[ord('a') - ord('a')] + form[ord('e') - ord('a')]:
            if i[0][1] == form[ord('k') - ord('a')][0]:
                rank[0][2] = i[0][1]
                break

    # con概率高于mon 猜测cm(cm同一频段已完成猜测)
    for i in triple_frequency:
        if i[0][1:] == form[ord('o') - ord('a')] + form[ord('n') - ord('a')]:
            if i[0][0] not in form:
                rank[0][0] = i[0][0]
                rank[0][4] = form[ord('m') - ord('a')][0] if form[ord('m') - ord('a')][0] != i[0][0] else form[ord('m') - ord('a')][1]
                break

    # 根据joy 判断j
    for i in triple_frequency:
        if i[0][1:] == form[ord('o') - ord('a')] + form[ord('y') - ord('a')]:
            if i[0][0] not in form and i[0][0] not in rank[0]:
                rank[0][1] = i[0][0]
                break

    # 根据ext 判断x
    for i in triple_frequency:
        if i[0][0] + i[0][2] == form[ord('e') - ord('a')] + form[ord('t') - ord('a')]:
            if i[0][1] not in form and i[0][1] not in rank[0]:
                rank[0][6] = i[0][1]
                break

    # 根据que 判断q，剩下z
    for i in triple_frequency:
        if i[0][1:] == form[ord('u') - ord('a')] + form[ord('e') - ord('a')]:
            if i[0][0] not in form and i[0][0] not in rank[0]:
                rank[0][5] = i[0][0]
                for item in form[ord('z') - ord('a')]:
                    if item not in rank[0]:
                        rank[0][7] = item
                        break
                break
    return form, rank


def final_sort(rank, signle):
    # 0, 1, 2, 3, 4, 5, 6, 7
    # c, j, k, l, m, q, x, z
    frequency = {}
    for i in range(8):
        frequency[rank[0][i]] = signle[rank[0][i]]
    frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=False)

    for i in range(1, 16):
        for j in range(9):
            rank[i][j] = rank[0][j]
    # 由单字母的概率分布，在最后的猜测中
    # lcm可能会出错，kjxqz会出错
    # cm出错概率最大
    rank[1][0], rank[1][4] = rank[1][4], rank[1][0]
    # all acc lc 可能会出错
    rank[2][3], rank[2][0], rank[2][8] = rank[2][0], rank[2][3], 1
    # lcm
    rank[3][3], rank[3][0], rank[3][4], rank[3][8] = rank[3][0], rank[3][4], rank[3][3], 2
    # 最后由还原度来排序
    # 字母频率越小，还原度越高（错误的个数少）
    for i in range(4, 16):
        for j in range(5):
            for k in range(j + 1, 5):
                rank[i][rank[0].index(frequency[j][0])], rank[i][rank[0].index(frequency[k][0])] = \
                    rank[i][rank[0].index(frequency[k][0])], rank[i][rank[0].index(frequency[j][0])]
                rank[i][8] = frequency[j][1] + frequency[j][1]
                for l in range(j + 1, 5):
                    rank[i][rank[0].index(frequency[j][0])], rank[i][rank[0].index(frequency[k][0])], rank[i][rank[0].index(frequency[l][0])] = \
                        rank[i][rank[0].index(frequency[k][0])], rank[i][rank[0].index(frequency[l][0])], rank[i][rank[0].index(frequency[j][0])]
                    rank[i][8] = frequency[j][1] + frequency[k][1] + frequency[l][1]
    rank = sorted(rank, key= lambda x: x[8], reverse=False)
    return rank


# s = input().strip()
with open('data.txt', 'r') as f:
    s = f.read()

single_frequency, double_frequency, triple_frequency, single = statistics(s)

form = single_letter_predict(single_frequency)

form = double_letter_predict(form, double_frequency)

form = triple_letter_predict(form, triple_frequency)

form, rank = frequency_guess(form, triple_frequency)

rank = final_sort(rank, single)

for i in range(10):
    k = 0
    print(i + 1, end=':')
    for j in range(26):
        if type(form[j]) == list:
            print(rank[i][k], end='')
            k += 1
        else:
            print(form[j], end='')
    print()