from glob import glob

links_file = glob('./links/*')
links_count = 0

data_file = glob('./data/*')
data_count = 0

for single_link in links_file:
    file = open(single_link,'r').readlines()
    links_count += len(file)

print('link files count: ' + str(len(links_file)))

print('links count: ')
print(links_count)

for single_data_file in data_file:
    current_file = open(single_data_file,'r',encoding='utf-8')

    for single_line in current_file.readlines():
        if single_line.find('word:') > -1:
            data_count += 1

print('data file count: ' + str(len(data_file)))
print('data count: ')
print(data_count)