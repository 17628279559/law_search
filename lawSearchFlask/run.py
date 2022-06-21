# -*- coding:utf-8 -*-
from flask import Flask, jsonify, request
from werkzeug.serving import make_server
from func import law
import re
import appbk_sql
import json
from copy import deepcopy

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['FLASK_ENV'] = 'production'
myLaw = law()

res = {
    'length': 0,
    'data': {},
    'message': '',
    'code': 200
}


@app.route('/getlawcount', methods=['get'])
def getlawcount():
    sql = "select * from lawcount"
    r = appbk_sql.mysql_com(sql)
    res1 = {}
    for i in r:
        res1[i['legalProvince']] = i['lawcount']
    with open("aliChina.json", "r", encoding="utf-8") as f:
        res2 = json.load(f)
    res = {
        'data1': res1,
        'data2': res2,
    }
    return jsonify(res)


@app.route('/getlawdata', methods=['POST'])
def getlawdata():
    words = request.form.get('words')
    words = myLaw.clean(words)
    if re.search(r'[^\u4e00-\u9fa5&|\-]', words):
        tmpres = deepcopy(res)
        tmpres['message'] = "含有非法字符,只能输入汉字和&|-以及空格"
        tmpres['code'] = 412
        return jsonify(tmpres)

    bool_operations = ["&", "|", "-"]
    bool_stack = [[]]

    bool_operation = "#"
    index = 0
    for i, word in enumerate(words):
        if word not in bool_operations:
            continue
        else:
            if words[index:i]:
                bool_stack.append([bool_operation, words[index:i]])
                bool_operation = words[i]
                index = i+1
    if words[index:len(words)]:
        bool_stack.append([bool_operation, words[index:len(words)]])
    result = myLaw.func_law_search(bool_stack)
    tmpres = deepcopy(res)
    if result:
        tmpres['message'] = "查询成功"
        tmpres['data'] = result
    else:
        tmpres['message'] = "未查询到相关数据"
        tmpres['code'] = 203
    return jsonify(tmpres)


if __name__ == "__main__":
    server = make_server('127.0.0.1', 8001, app)
    server.serve_forever()
    app.run()
