# -*- coding:utf-8 -*-
import jieba
import appbk_sql
import collections
import json
import re

# with open('stop_word.txt', 'r', encoding="utf-8") as f:
#     stopwords = f.read().split('\n')

# sql = "select id,legalPolicyName from law"
# res = appbk_sql.mysql_com(sql)


# def myjieba(text):
#     object_list = []
#     for word in text:
#         if word not in stopwords:
#             object_list.append(word)
#     word_counts = collections.Counter(object_list)
#     return word_counts


# resault = {}
# for i in res:
#     jiebadict = dict(myjieba(i['legalPolicyName']))
#     for j in jiebadict.keys():
#         if len(j) < 1:
#             continue
#         else:
#             if j in resault.keys():
#                 resault[j].append(str(i['id']))
#             else:
#                 resault[j] = [str(i['id'])]

# with open('1.json', 'w', encoding="utf-8") as f:
#     json.dump(resault, f, ensure_ascii=False)

words = jieba.lcut("大学生运动", cut_all=False, HMM=True)

print(words)
