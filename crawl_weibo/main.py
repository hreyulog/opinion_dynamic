import json
from get_comments import get_comments
from sentiment import sentiment,old_sentiment

from weiboSpider.weibo_spider.spider import Spider


class opinion:
    def __init__(self, user_id):
        self.user_id = user_id
        with open('config.json') as f:
            self.config = json.loads(f.read())
        self.config[
            'cookie'] = "WEIBOCN_FROM=1110006030; SUB=_2A25LNyDUDeRhGeFG7FUU8yfOyDmIHXVoTTwcrDV6PUJbkdAbLVf1kW1NeMEjPnL0iq3ovu_Up8PVOgWsa6oi0WXl; MLOGIN=1; _T_WM=47293913224; XSRF-TOKEN=731285; mweibo_short_token=8d71cbc576; M_WEIBOCN_PARAMS=uicode%3D20000174"
        self.config['user_id_list'] = [user_id]
        self.config['since_date'] = "2023-02-01"
        self.config['end_date'] = "2023-11-02"
        self.config['write_mode'] = ["csv"]
        # self.crawl_blogs()
        get_comments(user_id)
        # sentiment(user_id)
        # old_sentiment(user_id)

    def crawl_blogs(self):
        wb = Spider(self.config)
        wb.start(0)


if __name__ == "__main__":
    # 2245266941
    # 2561744167
    # for id in ['1783497251']:
    #     opinion(id)
    # opinion('')
    # had=['2022252207','2561744167','5821279480']
    with open('list_crawler.txt', 'r', encoding='utf-8') as reader:
        for row in reader:
            id = row.split()[1]
            Opinion = opinion(id)
