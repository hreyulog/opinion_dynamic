import csv
import json
from snownlp import SnowNLP

def sentiment(user_id):
    dict_blog = {}
    dict_score_comment = {}
    with open('weibo/comment' + user_id + '.csv.json', 'r', encoding='utf-8') as reader1:
        for row in reader1:
            json_row = json.loads(row)
            comment = json_row['comment']['comment']
            comment_likes = json_row['comment']['likes']
            id = json_row['id']
            if id not in dict_blog:
                dict_blog[id] = {'content': json_row['content'], 'likes': json_row['likes'], 'time': json_row['time']}
            if comment == "":
                score_comment = 0.5
            else:
                score_comment = SnowNLP(comment).sentiments
            if id not in dict_score_comment:
                dict_score_comment[id] = [(score_comment, comment_likes)]
            else:
                dict_score_comment[id].append((score_comment, comment_likes))

    with open(user_id+'output.json', 'w', encoding='utf-8') as writer:
        for id in dict_blog:
            writer.write(json.dumps({'id': id,
                                     'content': dict_blog[id]['content'],
                                     'content_score': SnowNLP(dict_blog[id]['content']).sentiments,
                                     'time': dict_blog[id]['time'],
                                     'likes': dict_blog[id]['likes'],
                                     'comment_score': dict_score_comment[id]
                                     }, ensure_ascii=False))
            writer.write('\n')


if __name__ == "__main__":
    sentiment('6048569942')
