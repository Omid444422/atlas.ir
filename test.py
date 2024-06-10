file = open('.\\data\\600 for IELTS_links.txt','r',encoding='utf-8')

counter = 0

for line in file.readlines():
    if line.find('word: ') > -1:
        counter += 1

print(counter)