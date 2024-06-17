import json
from datetime import datetime


def getmonday(st):
    date = datetime.strptime(st, '%Y-%m-%d')
    month = str(date.month)
    if len(month) == 1:
        month = '0' + month
    if (date.day - 1) // 15 == 0:
        return f'{date.year}-{month}-01'
    else:
        return f'{date.year}-{month}-16'


def check(user_id):
    for pi in ['huawei']:
        times = ['2023-11-01', '2023-10-16']
        with open('comment' + user_id + pi + '.json', 'r', encoding='utf-8') as reader1:
            with open('comment' + user_id + 'csv.json', 'w', encoding='utf-8') as writer:
                for row in reader1:
                    json_row = json.loads(row)
                    t = getmonday(json_row['time'].split()[0])
                    if t in times:
                        writer.write(json.dumps(json_row, ensure_ascii=False))
                        writer.write('\n')

        # print(pi)


if __name__ == "__main__":
    with open('list_crawler.txt', 'r', encoding='utf-8') as reader:
        for row in reader:
            id = row.split()[1]
            check(id)
