import json
from datetime import datetime
pinpai=['huawei','xiaomi','pingguo']
def getmonday(st):
    date = datetime.strptime(st, '%Y-%m-%d')
    month = str(date.month)
    if len(month) == 1:
        month = '0' + month
    if (date.day - 1) // 15 == 0:
        return f'{date.year}-{month}-01'
    else:
        return f'{date.year}-{month}-16'

time_list=['2024-04-16','2024-04-01', '2024-03-16', '2024-03-01', '2024-02-16', '2024-02-01', '2024-01-16', '2024-01-01', '2023-12-16', '2023-12-01','2023-11-16','2023-11-01']
print(len(time_list))

def check(user_id):
    for pi in pinpai:
        times=[]
        with (open('comment'+user_id + pi + '.json', 'r', encoding='utf-8') as reader1):
            for row in reader1:
                json_row = json.loads(row)
                t=getmonday(json_row['time'].split()[0])
                if t not in times:
                    times.append(t)
            for ti in time_list:
                if ti not in times:
                    print(user_id,pi)
                    print(times)
        # print(pi)
        # if pi=='huawei':
        # print(times)

if __name__=="__main__":
    with open('list_crawler.txt', 'r', encoding='utf-8') as reader:
        for row in reader:
            id = row.split()[1]
            check(id)