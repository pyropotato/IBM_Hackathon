f1 = open('common_tags/common_tags_03_31.txt','r')
f2 = open('common_tags/common_tags_30.txt','r')
f3 = open('common_tags/common_tags_29.txt','r')
f4 = open('common_tags/common_tags_04_01.txt','r')
f5 = open('common_tags/common_tags_04_02.txt','r')
f = open('final_comm_words', 'w')
x = [f1, f2, f3, f4, f5]

word_set = set()

for i in x:
    hashtags = i.readline()
    hashtags = hashtags.split(" ")
    for tag in hashtags:
        word_set.add(tag)

for i in word_set:
    f.write(i + " ")

f.close()