from sys import stdin
word_dic = {}
word_list = []
def seperate(word):
    for i in range(1, len(word) + 2):
        str = word[:i]
        fir = str[0: len(str) - 1]
        mid = str
        las = str[-1]
        if fir == "":
            fir = "0"
        word_dic[str] = "(" + fir + " (" + mid + " " + las +"))"
print('1')
for line in stdin:
    word_list.append(line.strip().replace(" ", ""))
for i in range(len(word_list)):
    seperate(word_list[i])
for i in word_dic.values():
    print(i)
for i in range(len(word_list)):
    print("(" + word_list[i] + " (" + '1' + " " + '*e*' +"))")
print('(1 (0 _))')