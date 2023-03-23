def letter_frequency_attack(s):
    count = {chr(i + ord('a')): 0 for i in range(26)}
    for i in s:
        count[i] += 1
    value = max(count, key=count.get)
    return (ord(value) - ord('e')) % 26


s = input().strip()
print(letter_frequency_attack(s))

