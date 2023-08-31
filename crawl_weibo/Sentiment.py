import csv
import json
import re
import jieba
from snownlp import SnowNLP


# 基于词典的情感识别
# class DictBasedSentAnal:
#
#     # 加载情感词典
#     def __init__(self):
#         self.__sent_dict__ = self.__read_dict('BosonNLP_sentiment_score.txt')
#
#     def analyse(self, sentence):
#         score = 0.0
#         for word in jieba.cut(sentence):
#             score += self.__sent_dict__.get(word, 0)
#         return score
#
#     @staticmethod
#     def __read_dict(path, encoding='utf-8'):
#         sent_dict = {}
#         with open(path, encoding=encoding) as input_file:
#             for line in input_file:
#                 array = re.split('\s+', line.strip())
#                 if len(array) == 2:
#                     sent_dict[array[0]] = float(array[1])
#         return sent_dict


if __name__ == "__main__":
    # Sentiment = DictBasedSentAnal()
    dict_time = {}
    dict_score_comment = {}
    dict_content = {}
    with open('6048569942.csv', 'r', encoding='utf-8') as reader2:
        csv_reader2 = csv.DictReader(reader2)
        for row in csv_reader2:
            id_weibo, content, time = row['\ufeff微博id'], row['微博正文'], row['发布时间']
            if 'huawei' in content or '华为' in content:
                if content != '':
                    dict_time[id_weibo] = time
    with open('comment6048569942.csv.json', 'r', encoding='utf-8') as reader1:
        for row in reader1:
            json_row = json.loads(row)
            id, content, comment = json_row['id'], json_row['content'], json_row['comment']['comment']
            if comment == "":
                score_comment = 0.5
            else:
                score_comment = SnowNLP(comment).sentiments
            dict_content[id] = content
            if id not in dict_score_comment:
                print(id)
                # dict_score_comment[id] = [{comment: score_comment}]
                dict_score_comment[id] = [score_comment]

            else:
                dict_score_comment[id].append(score_comment)
    with open('purecontent_sentiment.json', 'w', encoding='utf-8') as writer:
        for id in dict_time:
            writer.write(json.dumps({'id': id,
                                     'content': dict_content[id],
                                     'content_score':SnowNLP(dict_content[id]).sentiments,
                                     # 'content': {dict_content[id]: SnowNLP(dict_content[id]).sentiments},
                                     'time': dict_time[id],
                                     # 'sum_comment_score': sum(
                                     #     [dict_score_comment[id][i] for i in dict_score_comment[id]]),
                                     'avg_score': sum(dict_score_comment[id]) / len(dict_score_comment[id]),
                                     'comment_score': dict_score_comment[id]
                                     }, ensure_ascii=False))
            writer.write('\n')
        # Sentiment.analyse()
