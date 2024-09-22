import csv
with open('1783497251.csv','r',newline='',encoding='utf-8') as reader:
    csv_reader=csv.reader(reader,delimiter=',')
    for row in csv_reader:
        if 'huawei' in row[1] or '华为' in row[1]:
            print(row)