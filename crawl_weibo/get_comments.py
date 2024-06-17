import csv
import json
import re

import requests

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
headers = {'User_Agent': user_agent,
           'cookie': "WEIBOCN_FROM=1110006030; _T_WM=19135211362; SCF=AnztgX4oKCLbIbB1eDU_hCTt_VGGlmd1lvu7XWA1q0LGUZJaUC-ReY492bbEIk8uDpcyF-R53fKNKB2sn9jGG9s.; SUB=_2A25LRzwPDeRhGeFG7FUU8yfOyDmIHXVoPTHHrDV6PUJbktAbLUHjkW1NeMEjPgsAIgGq1njZRZFzT7vY2-DCml6z; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W59zBl._dzhJIHPO0wPOXmc5NHD95QN1hMNSKe4eoefWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0nNS0-01Kz0SBtt; SSOLoginState=1715686495; ALF=1718278495; XSRF-TOKEN=ae008e; MLOGIN=1; mweibo_short_token=be9f7de7f8; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174"
           }
def writetheme(pinpai, dict_weibo, filename):
    with open('weibo/comment' + filename + pinpai + '.json', 'w', encoding='utf-8') as writer:
        for id in dict_weibo:
            print(id)
            page = 1
            max_id = ''
            while True:
                if page == 1:  # 第一页，没有max_id参数
                    url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(id, id)
                else:  # 非第一页，需要max_id参数
                    if max_id == "0":  # 如果发现max_id为0，说明没有下一页了，break结束循环
                        print('max_id is 0, break now')
                        break
                    url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0&max_id={}'.format(id, id,
                                                                                                            max_id)
                print(url)
                r = requests.get(url, headers=headers)
                print(r.status_code)
                if r.status_code==500:
                    break
                if r.json()['ok'] == 0:
                    break
                datas = r.json()['data']['data']
                for data in datas:
                    dr = re.compile(r'<[^>]+>', re.S)  # 用正则表达式清洗评论数据
                    text2 = dr.sub('', data['text'])
                    this_dict = {
                        'id': id,
                        'content': dict_weibo[id]['content'],
                        'time': dict_weibo[id]['time'],
                        'likes': dict_weibo[id]['likes'],
                        'comment': {'id': data['user']['id'], 'comment': text2, 'time': data['created_at'],
                                    'likes': data['like_count']},
                    }
                    writer.write(json.dumps(this_dict, ensure_ascii=False))
                    writer.write('\n')
                page += 1
                max_id = str(r.json()['data']['max_id'])


def checkhuawei(content):
    return 'huawei' in content or '华为' in content or 'nova' in content


def checkxiaomi(content):
    return 'xiaomi' in content or '小米' in content or '米家' in content


def checkpingguo(content):
    return 'apple' in content or '苹果' in content or 'iphone' in content or 'ipad' in content or 'mac' in content


def get_comments(user_id):
    dict_weibo_huawei = {}
    dict_weibo_xiaomi = {}
    dict_weibo_pingguo = {}
    dict_weibo_all = {}
    filename = user_id + '.csv'
    with open('weibo/' + filename, 'r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            id_weibo, content, time, likes = row['微博id'], row['微博正文'], row['发布时间'], row['点赞数']
            content = content.lower()
            if checkhuawei(content) and checkpingguo(content) and checkxiaomi(content):
                dict_weibo_all[id_weibo] = {'content': content, 'time': time, 'likes': likes}
            if checkhuawei(content):
                dict_weibo_huawei[id_weibo] = {'content': content, 'time': time, 'likes': likes}
            elif checkxiaomi(content):
                dict_weibo_xiaomi[id_weibo] = {'content': content, 'time': time, 'likes': likes}
            elif checkpingguo(content):
                dict_weibo_pingguo[id_weibo] = {'content': content, 'time': time, 'likes': likes}
    # writetheme(pinpai='huawei', dict_weibo=dict_weibo_huawei, filename=user_id)
    writetheme(pinpai='xiaomi', dict_weibo=dict_weibo_xiaomi, filename=user_id)
    writetheme(pinpai='pingguo', dict_weibo=dict_weibo_pingguo, filename=user_id)
    # writetheme(pinpai='all', dict_weibo=dict_weibo_all, filename=user_id)


if __name__ == "__main__":
    get_comments('7239083016')
