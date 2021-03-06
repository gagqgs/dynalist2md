#!/usr/bin/env python3
# Dynalist to Markdown

import requests
import json
import os
import sys

#
# const
#
Dynalist_API = 'https://dynalist.io/api/v1'

#
# 環境変数からAPI_secret_tokenを取得
#
API_secret_token = os.getenv("Dynalist_API_KEY", "")
if API_secret_token == "":
    print("You need to set Dynalist_API_KEY in .bashrc!")
    sys.exit(1)


def get_body(file_id):
    API_URL = Dynalist_API + '/doc/read'

    header = {"Content-Type" : "application/json"}
    payload = {
		'token': API_secret_token,
		'file_id': file_id
	}
    res = requests.post(API_URL, json.dumps(payload), headers=header)
    json_data = res.json()
    return json_data

#
# root（file_data['nodes'])からtext_listを生成する[(id, text), ...]
#
def build_element_list(root):
    element_list = []
    for node in root:
        if 'children' in node:
            children =  node['children']
        else:
            children = None
        element_list.append((node['id'], node['content'], node['checked'], node['note'], children))
        #print((node['id'], node['content']))
    return element_list


#
# text_listとidからtextを抽出
#
def lookup_element(element_list, id):
    for t in element_list:
        if id == t[0]:
                return t
    return ''


#
# 順序でリストを作る
#
def each_list_order(element_list, text_list, id, children, indent_lv):
    for l in children:
        element = lookup_element(element_list, l)
        #print(element)
        text = element[1].strip()
        if text == '':
            pass
        elif text.startswith('---'):
            pass
        else:
            text_list.append((indent_lv, text, element[2], element[3]))

        if element[4] is not None:
            #print(element[4], indent_lv + 1)
            each_list_order(element_list, text_list, element[0], element[4], indent_lv + 1)


def do_list_order(element_list, file_data):
    indent_lv = 0
    text_list =  []
    text_list.append((indent_lv,file_data['nodes'][0]['content'].strip(), file_data['nodes'][0]['checked'], file_data['nodes'][0]['note']))
    #print(indent_lv, file_data['nodes'][0]['content'])

    each_list_order(element_list, text_list, file_data['nodes'][0]['id'], file_data['nodes'][0]['children'], indent_lv + 1)

    return text_list


def export_text(text):
    if text.startswith('#'):
        return '\\' + text
    elif text.startswith('---'):
        return '\n'
        # return '\n' + text + '\n'
    else:
        return text


def text_export(text_list):
    for n in range(0, len(text_list)):
        print(text_list[n][0], text_list[n][1])


def text_list_to_markdown(text_list):
    for n in range(0, len(text_list) -1):
        #print(text_list[n][0], text_list[n][1])
        current_lv = text_list[n][0]
        next_lv    = text_list[n+1][0]

        if current_lv == next_lv:
            print(export_text(text_list[n][1]))
        elif current_lv < next_lv:
            print()
            print('#' * next_lv + ' '  + export_text(text_list[n][1]))
            print()
        else:
            print(export_text(text_list[n][1]))
            print()
    print(export_text(text_list[n + 1][1]))


def text_format(text_list):
    for line in text_list:
        print(line[0], line[1])


def main(id):

    file_data = get_body(id)
    if file_data is None:
        print("Can't find file")
        sys.exit(1)

    element_list = build_element_list(file_data['nodes'])
    text_list = do_list_order(element_list, file_data)

    #text_export(text_list)
    #text_format(text_list)
    #text_export(text_list)

    text_list_to_markdown(text_list)
    return


if __name__ == "__main__":

    if len(sys.argv) == 2:
        main(sys.argv[1])
        sys.exit(0)

    else:
        print(sys.argv[0] + "'file_id' -> convert to markdown")
        sys.exit(1)
