# -*- coding:utf-8 -*-
import appbk_sql
import json
import re
import jieba


class law:
    def __init__(self):
        with open("Inverted_Index.json", encoding="utf-8") as f1:
            self.data = json.load(f1)
        with open("words.json", encoding="utf-8") as f2:
            self.allwords = json.load(f2)
        self.allwordskey = self.allwords.keys()
        self.keys = self.data.keys()
        self.select_laws_by_id = 'SELECT `id`,`legalPolicyName`,`legalProvince`,`legalPublishedTime`,`legalDocumentNumber`,`legalPolicyText`,`legalUrl` FROM `law` WHERE `id` IN ({})'
        self.select_laws_by_similarity = 'SELECT `id` FROM `law` WHERE legalPolicyName LIKE "%{}%"'

    def clean(self, words):
        sub = re.sub(r'[\t\r\n\s]', '', words)
        sub = sub.replace('\u3000', '').replace('\xa0', '').replace('&nbsp;', '')
        return sub

    def get_laws(self, id_list):
        if id_list:
            return appbk_sql.mysql_com(self.select_laws_by_id.format(",".join(id_list)))

    def get_laws_by_word(self, word):
        if word in self.keys:
            res = self.data[word]
        else:
            words = jieba.lcut(word, cut_all=False, HMM=True)
            if len(words) == 1:
                res = self.get_id_by_all_words(word[0])
                for i in word[1:]:
                    res = list(set(res) & set(self.get_id_by_all_words(i)))
            else:
                b_stack = [[], ["#", words[0]]]
                for i in words[1:]:
                    b_stack.append(["&", i])
                res = self.get_laws_by_bool(b_stack)

        return res

    def get_id_by_all_words(self, word):
        if word in self.allwordskey:
            return self.allwords[word]
        else:
            return []

    def get_laws_by_or(self, id_list, word):
        nid_list = self.get_laws_by_word(word)
        return list(set(id_list) | set(nid_list))

    def get_laws_by_and(self, id_list, word):
        nid_list = self.get_laws_by_word(word)
        return list(set(id_list) & set(nid_list))

    def get_laws_by_not(self, id_list, word):
        nid_list = self.get_laws_by_word(word)
        return list(set(id_list) - set(nid_list))

    # 定义布尔检索栈，栈顶为当前id列表，其余为项为[操作符,关键词]
    # 如 北京 & 教育 输入为 [[],["#","北京"],["&","教育"]]
    def get_laws_by_bool(self, bool_stack):

        if len(bool_stack) == 1:
            return bool_stack[0]
        else:
            if bool_stack[1][0] == "#":
                bool_stack[1] = self.get_laws_by_word(bool_stack[1][1])
                return self.get_laws_by_bool(bool_stack[1:])
            if bool_stack[1][0] == "&":
                bool_stack[1] = self.get_laws_by_and(bool_stack[0], bool_stack[1][1])
                return self.get_laws_by_bool(bool_stack[1:])
            if bool_stack[1][0] == "|":
                bool_stack[1] = self.get_laws_by_or(bool_stack[0], bool_stack[1][1])
                return self.get_laws_by_bool(bool_stack[1:])
            if bool_stack[1][0] == "-":
                bool_stack[1] = self.get_laws_by_not(bool_stack[0], bool_stack[1][1])
                return self.get_laws_by_bool(bool_stack[1:])

    def func_law_search(self, bool_stack):
        return self.get_laws(self.get_laws_by_bool(bool_stack))

# myLaw = law()
# result = myLaw.get_laws_by_bool([[], ["#", "儿童关爱"]])
# print(result)
