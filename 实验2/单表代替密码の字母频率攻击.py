class get_out_of_loop(Exception):
    pass


def statistics(s, single, double, triple):
    for i in range(len(s) - 2):  # 为了方便2/3阶统计，少个字母也没事（）
        single[s[i]] += 1
        double[s[i] + s[i+1]] += 1
        triple[s[i] + s[i+1] + s[i+2]] += 1
    single_frequency = sorted(single.items(), key=lambda x: x[1], reverse=True)
    double_frequency = sorted(double.items(), key=lambda x: x[1], reverse=True)
    triple_frequency = sorted(triple.items(), key=lambda x: x[1], reverse=True)
    return single_frequency, double_frequency, triple_frequency


def single_letter_predict(single_frequency):
    frequency_letter = ['e', 't', 'a', 'o', 'i', 'n',
                        's', 'r', 'h', 'l', 'd', 'c',
                        'u', 'm', 'f', 'p', 'g', 'w', 'y',
                        'b', 'v', 'k', 'x', 'j', 'q', 'z']
    result = [[] for i in range(26)]
    # 根据字母频率表，将密文对应的字母填入，因有多个字母频率相近
    # 故将所有可能性都填入列表中，后续进行选择排除
    result[ord(frequency_letter[0]) - ord('a')] = single_frequency[0][0]
    for i in range(1, 4):
        for j in range(1, 4):
            result[ord(frequency_letter[j]) - ord('a')].append(single_frequency[i][0])
    for i in range(4, 9):
        for j in range(4, 9):
            result[ord(frequency_letter[j]) - ord('a')].append(single_frequency[i][0])
    for i in range(9, 11):
        for j in range(9, 11):
            result[ord(frequency_letter[j]) - ord('a')].append(single_frequency[i][0])
    for i in range(11, 20):
        for j in range(11, 20):
            result[ord(frequency_letter[j]) - ord('a')].append(single_frequency[i][0])
    for i in range(20, 22):
        for j in range(20, 22):
            result[ord(frequency_letter[j]) - ord('a')].append(single_frequency[i][0])
    for i in range(22, 26):
        for j in range(22, 26):
            result[ord(frequency_letter[j]) - ord('a')].append(single_frequency[i][0])
    return result


def remove(form, letter):
    for i in form:
        if type(i) == list:
            if letter in i:
                i.remove(letter)
                if len(i) == 1:
                    form[form.index(i)] = i[0]
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
        for i in range(8):
            for j in range(i + 1, 9):
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
                    for l in range(k + 1, 15):
                        if double_frequency[i][0][1] == double_frequency[j][0][1] == double_frequency[k][0][1] == double_frequency[l][0][1]:
                            form[ord('n') - ord('a')] = double_frequency[i][0][1]  # 判断出n
                            form = remove(form, double_frequency[i][0][1])
                            list_ = [i, j, k, l]
                            for x in list_:  # 移除e
                                if double_frequency[x][0][0] == form[ord('e') - ord('a')]:
                                    list_.remove(x)
                                    break
                            for x in list_:  # 判断出i
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
    # 判断d 由ed判断
    for i in range(30):
        if double_frequency[i][0][0] == form[ord('e') - ord('a')]:
            if double_frequency[i][0][1] not in form:
                form[ord('d') - ord('a')] = double_frequency[i][0][1]
                form = remove(form, double_frequency[i][0][1])
                break

    # 判断u
    for i in range(30):
        if double_frequency[i][0][0] == form[ord('o') - ord('a')]:
            if double_frequency[i][0][1] not in form:
                form[ord('u') - ord('a')] = double_frequency[i][0][1]
                form = remove(form, double_frequency[i][0][1])
                break
    # 判断g
    for i in range(30):
        if double_frequency[i][0][0] == form[ord('n') - ord('a')]:
            if double_frequency[i][0][1] not in form:
                form[ord('g') - ord('a')] = double_frequency[i][0][1]
                form = remove(form, double_frequency[i][0][1])
                break
    # 判断f
    for i in range(40):
        if double_frequency[i][0][0] == form[ord('o') - ord('a')]:
            if double_frequency[i][0][1] not in form:
                form[ord('f') - ord('a')] = double_frequency[i][0][1]
                form = remove(form, double_frequency[i][0][1])
                break

    return form


def triple_letter_predict(form, triple_frequency):
    # 根据三字母单词判断单词 b,c,j,k,m,p,q,v,w,x,y,z
    # 剩下未确定的字母为
    # 根据was 判断w
    for i in triple_frequency:
        if i[0][1:] == form[ord('a') - ord('a')] + form[ord('s') - ord('a')]:
            if i[0][0] not in form:
                form[ord('w') - ord('a')] = i[0][0]
                form = remove(form, i[0][0])
                break

    # 根据ver 判断v，因kv在同一频率段可同时判断出k
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

    # 剩下未确定字母 c,j,m,p,q,x,z
    # 根据pre概率最高判断出p
    for i in triple_frequency:
        if i[0][1:] == form[ord('r') - ord('a')] + form[ord('e') - ord('a')]:
            if i[0][0] not in form:
                form[ord('p') - ord('a')] = i[0][0]
                form = remove(form, i[0][0])
                break

    # 根据act概率高判断出c 因cm在同一频率段可同时判断出m
    for i in triple_frequency:
        if i[0][0] + i[0][2] == form[ord('a') - ord('a')] + form[ord('t') - ord('a')]:
            if i[0][1] not in form:
                form[ord('c') - ord('a')] = i[0][1]
                form = remove(form, i[0][1])
                break

    # 根据joy 判断j
    for i in triple_frequency:
        if i[0][1:] == form[ord('o') - ord('a')] + form[ord('y') - ord('a')]:
            if i[0][0] not in form:
                form[ord('j') - ord('a')] = i[0][0]
                form = remove(form, i[0][0])
                break

    # 根据exc 判断x
    for i in triple_frequency:
        if i[0][0] + i[0][2] == form[ord('e') - ord('a')] + form[ord('c') - ord('a')]:
            if i[0][1] not in form:
                form[ord('x') - ord('a')] = i[0][1]
                form = remove(form, i[0][1])
                break

    # 根据que 判断q，剩下z
    for i in triple_frequency:
        if i[0][1:] == form[ord('u') - ord('a')] + form[ord('e') - ord('a')]:
            if i[0][0] not in form:
                form[ord('q') - ord('a')] = i[0][0]
                form = remove(form, i[0][0])
                break
    return form


# s = input().strip()
with open('data.txt', 'r') as f:
    s = f.read()

single_frequency = {chr(i + ord('a')): 0 for i in range(26)}
double_frequency = {chr(i + ord('a')) + chr(j + ord('a')): 0 for i in range(26) for j in range(26)}
triple_frequency = {chr(i + ord('a')) + chr(j + ord('a')) + chr(k + ord('a')): 0 for i in range(26) for j in range(26) for k in range(26)}
single_frequency, double_frequency, triple_frequency = statistics(s, single_frequency, double_frequency, triple_frequency)

# form = single_letter_predict(single_frequency)
#
# form = double_letter_predict(form, double_frequency)
#
# form = triple_letter_predict(form, triple_frequency)

# print(form)
# key = ''
# for i in form:
#     key += i

# print("laksjdhfgpzoxicuvmqnwberyt")
