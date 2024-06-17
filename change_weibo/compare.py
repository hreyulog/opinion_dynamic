import json

import csv
import re

import requests

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
headers = {'User_Agent': user_agent,
           'cookie': "_T_WM=77341372861; SCF=ArwBbgYGS-iqpxaFehhbJNxigFFCyq_Ea-EVTsARvUjaMjcskiJQbDyQou3bC_9p3zMWD9qe29tK4secW5cymCY.; SUB=_2A25It_ElDeRhGeFN71oR9yzPzz-IHXVrzQztrDV6PUJbktANLXjZkW1NQA0nMSb2tXxeHBPsG07K_Z2RM4BbaxgH; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWOd-2y5aQMBANronYeI7nO5JpX5KzhUgL.FoM0Shn7S0z0She2dJLoI7yQMJH4Ugpa97tt; ALF=1708854901; XSRF-TOKEN=e1cb9e; MLOGIN=1; WEIBOCN_FROM=1110106030; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174"
           }


def read_row(row):
    row_dict = json.loads(row)
    post_id = row_dict['id']
    post_likes = row_dict['likes']
    comment_id = row_dict['comment']['comment'] + str(row_dict['comment']['id'])
    comment_likes = row_dict['comment']['likes']
    if comment_likes == None:
        comment_likes = 0
    return post_id, int(post_likes), comment_id, int(comment_likes)


def compare_post(file1, file2):
    dict_weibo1 = {}
    dict_weibo2 = {}

    with open(file1, 'r', encoding='utf-8') as file1:
        csv_reader1 = csv.DictReader(file1)
        for row in csv_reader1:
            id_weibo, content, time, likes = row['\ufeff微博id'], row['微博正文'], row['发布时间'], row['点赞数']
            if 'huawei' in content or '华为' in content:
                dict_weibo1[id_weibo] = likes
    with open(file2, 'r', encoding='utf-8') as file2:
        csv_reader2 = csv.DictReader(file2)
        for row in csv_reader2:
            id_weibo, content, time, likes = row['\ufeff微博id'], row['微博正文'], row['发布时间'], row['点赞数']
            if 'huawei' in content or '华为' in content:
                dict_weibo2[id_weibo] = likes
    i = 0
    r = 0
    post_like1 = []
    post_like2=[]
    for id_wei in dict_weibo1:
        if id_wei in dict_weibo2:
            post_like1.append(int(dict_weibo1[id_wei]))
            post_like2.append(int(dict_weibo2[id_wei]))
        else:
            r += 1
    print('post1_likes:',sum(post_like1))
    print('post2_likes:',sum(post_like2))
    print('post_likes_change', ' ', abs(sum(post_like1)-sum(post_like2)) / sum(post_like1))
    print('post_remove', ' ', 0 / len(dict_weibo1))


def compare_comment(file1, file2):
    dict_post_likes_file1 = {}
    dict_post_likes_file2 = {}
    dict_comment_likes_file1 = {}
    dict_comment_likes_file2 = {}
    dict_post_comment = {}
    with open(file1, 'r', encoding='utf-8') as reader1:
        for row in reader1:
            if '回复@' not in row:
                post_id, post_likes, comment_id, comment_likes = read_row(row)
                if post_id not in dict_post_comment:
                    dict_post_comment[post_id] = [comment_id]
                else:
                    dict_post_comment[post_id].append(comment_id)
                dict_post_likes_file1[post_id] = post_likes
                dict_comment_likes_file1[comment_id] = comment_likes

    with open(file2, 'r', encoding='utf-8') as reader2:
        for row in reader2:
            if '回复@' not in row:
                post_id, post_likes, comment_id, comment_likes = read_row(row)
                dict_post_likes_file2[post_id] = post_likes
                dict_comment_likes_file2[comment_id] = comment_likes
    # print('post number:', len(dict_post_likes_file1), ' ', len(dict_post_likes_file2))
    # print('comment number:', len(dict_comment_likes_file1), ' ', len(dict_comment_likes_file2))
    notread = []
    for post_id in dict_post_likes_file1:
        if post_id not in dict_post_likes_file2:
            for comment_id in dict_post_comment[post_id]:
                notread.append(comment_id)

    # post_likes_different = 0
    # remove_post = 0
    # for post_id in dict_post_likes_file1:
    #     if post_id in dict_post_likes_file2:
    #         if dict_post_likes_file2[post_id] != dict_post_likes_file1[post_id]:
    #             post_likes_different += 1
    #             # post_likes_different += abs(dict_post_likes_file2[post_id] - dict_post_likes_file1[post_id])
    #     else:
    #         print(post_id)
    #         remove_post += 1
    # print('post_likes change:', post_likes_different, ' ', post_likes_different / len(dict_post_likes_file1))
    # # print('post_likes change:', post_likes_different, ' ', post_likes_different / sum(dict_post_likes_file1.values()))
    # print('post remove:', remove_post, ' ', remove_post / len(dict_post_likes_file1))
    comment1_likes = []
    comment2_likes = []
    comment_likes_different = 0
    remove_comment = 0
    for comment_id in dict_comment_likes_file1:
        if comment_id in dict_comment_likes_file2:
            comment1_likes.append(dict_comment_likes_file1[comment_id])
            comment2_likes.append(dict_comment_likes_file2[comment_id])
            # comment_likes_different += abs(dict_comment_likes_file1[comment_id])
        elif comment_id not in notread:
            remove_comment += 1
    print('comment_likes1:',sum(comment1_likes))
    print('comment_likes2:',sum(comment2_likes))
    print('comment_likes change:', ' ',
          abs(sum(comment1_likes) - sum(comment2_likes)) / sum(comment1_likes))
    # print('comment_likes change:', comment_likes_different, ' ',
    #       comment_likes_different / sum(dict_comment_likes_file1.values()))
    print('comment1:',len(dict_comment_likes_file1))
    print('comment2:', len(dict_comment_likes_file1)-remove_comment)
    print('comment remove:', ' ', remove_comment / len(dict_comment_likes_file1))


if __name__ == "__main__":
    # get_blog_likes('NDEIGnHwm')
    compare_comment('comment1783497251.csv.json', 'comment1783497251.csv_new.json')
    compare_post('1783497251.csv', '1783497251_new.csv')
