import json


def get_weighted_avg(dim2list):
    sum_all = 0
    cont = 0
    for row in dim2list:
        if row[1] == 0:
            row[1] = 1
        sum_all += row[0] * row[1]
        cont += row[1]
    return sum_all / cont


def get_oneday(dic):
    dict_byday = {}
    for time in dic:
        day = time.split(' ')[0]
        if day not in dict_byday:
            dict_byday[day] = dic[time]
        else:
            dict_byday[day] += dic[time]
    return dict_byday


def main(user_id):
    dict_time = {}
    dict_avg = {}
    with open(user_id + 'output.json', 'r', encoding='utf-8') as reader:
        for row in reader:
            json_row = json.loads(row)
            dict_time[json_row['time']] = json_row['comment_score']
    dict_byday = get_oneday(dict_time)
    for day in dict_byday:
        dict_avg[day] = get_weighted_avg(dict_byday[day])
    print(dict_avg)


if __name__ == "__main__":
    main('1871821935')
