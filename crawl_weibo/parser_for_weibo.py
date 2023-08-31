import csv
import json
import re

import requests

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
headers = {'User_Agent': user_agent,
           'cookie': "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWOd-2y5aQMBANronYeI7nO5JpX5KMhUgL.FoM0Shn7S0z0She2dJLoI7yQMJH4Ugpa97tt; SSOLoginState=1693312446; ALF=1695904446; SCF=ArwBbgYGS-iqpxaFehhbJNxigFFCyq_Ea-EVTsARvUjaYpQLNFye1LoQ_j5p2dObJjfY1XOSYMJebVrrZ8AzzwU.; SUB=_2A25J6ZXuDeRhGeFN71oR9yzPzz-IHXVrFTumrDV6PUNbktAGLWjdkW1NQA0nMZU5sPxgaH_sjfDW0sPzvqxYlO0n; _T_WM=04880d5f124d730ad5e2d22b35445f37"}


def main():
    dict_weibo = {}
    filename = '6048569942.csv'
    with open(filename, 'r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            id_weibo, content = row['\ufeff微博id'], row['微博正文']
            if 'huawei' in content or '华为' in content:
                dict_weibo[id_weibo] = content
    with open('comment' + filename + '.json', 'w', encoding='utf-8') as writer:
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
                r = requests.get(url, headers=headers)
                if r.json()['ok'] == 0:
                    break
                datas = r.json()['data']['data']
                for data in datas:
                    dr = re.compile(r'<[^>]+>', re.S)  # 用正则表达式清洗评论数据
                    text2 = dr.sub('', data['text'])
                    this_dict = {
                        'id': id,
                        'content': dict_weibo[id],
                        'comment': {'id': data['user']['id'], 'comment': text2, 'time': data['created_at']}
                    }
                    writer.write(json.dumps(this_dict, ensure_ascii=False))
                    writer.write('\n')
                page += 1
                max_id = str(r.json()['data']['max_id'])


if __name__ == "__main__":
    main()
