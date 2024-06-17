import json
from datetime import datetime
import os
import re

users = []
with open('list_crawler.txt', 'r', encoding='utf-8') as reader:
    for row in reader:
        id = row.split()[1]
        users.append(id)
def getmonday(st):
    date = datetime.strptime(st, '%Y-%m-%d')
    month = str(date.month)
    if len(month) == 1:
        month = '0' + month
    if (date.day - 1) // 15 == 0:
        return f'{date.year}-{month}-01'
    else:
        return f'{date.year}-{month}-16'



def check(filename):
    check_times=['2023-10-01', '2023-09-16', '2023-09-01', '2023-08-16', '2023-08-01', '2023-07-16', '2023-07-01', '2023-06-16', '2023-06-01', '2023-05-16']
    times=[]
    with (open(filename, 'r', encoding='utf-8') as reader1):
        for row in reader1:
            json_row = json.loads(row)
            t=getmonday(json_row['time'].split()[0])
            if t not in times:
                times.append(t)
        numbers = re.findall(r'\d+', filename)
        user_id=''.join(numbers)
        if user_id not in users:
            print(user_id)
            print(times)
        # print(pi)
        # if pi=='huawei':
        # print(times)

if __name__=="__main__":
    # 遍历目录
    for filename in os.listdir():
        if filename.endswith(".json"):
            check(filename)
