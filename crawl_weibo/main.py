import csv
import json

from sentiment import sentiment
from get_comments import get_comments

from weiboSpider.weibo_spider.spider import Spider


class opinion:
    def __init__(self, user_id):
        self.user_id = user_id
        with open('config.json') as f:
            self.config = json.loads(f.read())
        self.config[
            'cookie'] = "_T_WM=04880d5f124d730ad5e2d22b35445f37; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWOd-2y5aQMBANronYeI7nO5JpX5K-hUgL.FoM0Shn7S0z0She2dJLoI7yQMJH4Ugpa97tt; MLOGIN=1; SCF=ArwBbgYGS-iqpxaFehhbJNxigFFCyq_Ea-EVTsARvUjaKRWcE-9NLsoOA_uw2d6RIXS9Jy5xV7lZl4q2uNxM1zg.; SUB=_2A25J9BJHDeRhGeFN71oR9yzPzz-IHXVrFr4PrDV6PUJbktAGLU3FkW1NQA0nMSR2QgDPwwF4tiLOI8Y_rCzeHvc4; SSOLoginState=1693475352; ALF=1696067352; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D231051_-_followers_-_6048569942"
        self.config['user_id_list'] = [user_id]
        self.crawl_blogs()
        get_comments(user_id)
        sentiment(user_id)

    def crawl_blogs(self):
        wb = Spider(self.config)
        wb.start()


if __name__ == "__main__":
    with open('list_bozhu.txt', 'r', encoding='utf-8') as reader:
        for row in reader:
            id = row.split()[1]
            Opinion = opinion(id)
