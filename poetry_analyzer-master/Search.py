import sqlite3
from collections import defaultdict
import requests
import os
import json
def get_json_byid(id):
    try:
        r=requests.get('http://cbdb.fas.harvard.edu/cbdbapi/person.php?id=%s&o=json'%id).json()
    except:
        r=''
    return r


def search_authorsid_in_CDBD(db_file):
    tang_begin_year=618
    tang_end_year=907
    author_id=set()
    author_name=set()
    author_id_dict=defaultdict(set)
    conn=sqlite3.connect(db_file)
    cursor=conn.cursor()
    cursor.execute('select c_personid,c_name_chn, c_birthyear,c_deathyear FROM BIOG_MAIN WHERE c_birthyear>618 and c_deathyear<907')
    person_info_list=cursor.fetchall()
    return person_info_list

def get_KinshipInfo(dic):#查找血缘关系,并返回人物id、姓名、关系名
    person_name=[]
    person_re=[]
    person_id=[]
    #person_name.append(name)
    b=dic['Package']['PersonAuthority']['PersonInfo']['Person']['PersonKinshipInfo']['Kinship']
    for d in b:
        person_name.append(d['KinPersonName'])
    person_name=list(set(person_name))
    for a in person_name:
        for d in b:
            if(a==d['KinPersonName']):
                person_id.append(d['KinPersonId'])
                person_re.append(d['KinRelName'])
                break
    return person_id,person_name,person_re


def get_AssocInfo(dic):
    person_name = []
    person_re = []
    person_id = []
    b = dic['Package']['PersonAuthority']['PersonInfo']['Person']['PersonSocialAssociation']['Association']
    for d in b:
        person_name.append(d['AssocPersonName'])
    person_name=list(set(person_name))
    for a in person_name:
        for d in b:
            if (a == d['AssocPersonName']):
                person_id.append(d['AssocPersonId'])
                person_re.append(d['AssocName'])
                break
    return person_id, person_name, person_re

def get_data_for_single_grpha(person_name,n,person_re):
    data_text='data:[\n'
    data_item_format = "{name: '%s'},\n"
    for i in range(len(person_name)):
        data_text += data_item_format % (person_name[i])
    data_text+=data_item_format%(n)
    data_text+='],\n'
    links_text = 'links: [\n'
    links_item_format = """{source: '%s', target: '%s',label:'%s'
        },
       """
    for i in range(len(person_name)):
        links_text += links_item_format % (person_name[i],n,person_re[i])
    links_text += '],\n'
    return data_text,links_text
# def get_data_for_main_graph(CDBD):
#     person_name=[]
#     person_id=[]
#     person_re=[]
#     links_text = 'links: [\n'
#     links_item_format = """{source: '%s', target: '%s'
#             },
#            """
#     for n in CDBD:
#         person_id.append(n[0])
#     person_id=list(set(person_id))
#     for n in person_id:
#         d=get_json_byid(n)
#         # b=d['Package']['PersonAuthority']['PersonInfo']['Person']['BasicInfo']
#         # h=b['ChName']
#         # person_name.append(h)
#         c = d['Package']['PersonAuthority']['PersonInfo']['Person']['PersonKinshipInfo']['Kinship']
#         for m in c:
#             print(m['KinPersonId'])
#         #     if (m['AssocPersonId'] in person_id):
#         #         links_text += links_item_format % (m['AssocPersonName'], b['ChName'])
#         #print(person_name)
#     links_text += '],\n'
#     return links_text





def generate_html_page(data_text,links_text):
    saved_html_file='templates/person.html'
    html_dir = os.path.dirname(saved_html_file)
    html_head_path = os.path.join('static', 'html_head.txt')
    html_tail_path = os.path.join('static', 'html_tail.txt')
    with open(html_head_path, 'r', encoding='utf-8') as f:
        head_text = f.read()
    with open(html_tail_path, 'r', encoding='utf-8') as f:
        tail_text = f.read()
        # 合并存储为html
    with open(saved_html_file, 'w', encoding='utf-8') as f:
        f.write(head_text + data_text + links_text + tail_text)

if __name__ == '__main__':
    id=3332
    b=search_authorsid_in_CDBD('static/cbdb_sqlite.db')
    a=get_json_byid(id)
    # for r in b:
    #     if(r[0]==id):
    #         c=r[1]
    # person_name=[]
    # person_re=[]
    # person_id=[]
    # person_id,person_name,person_re=get_KinshipInfo(a)
    # data_text,links_text=get_data_for_single_grpha(person_name,c,person_re)
    # generate_html_page(data_text,links_text)
    # c=a['Package']['PersonAuthority']['PersonInfo']['Person']['PersonSocialAssociation']['Association']
    # for d in c:
    #     print(d['AssocPersonId'])
    # c=get_data_for_main_graph(b)
    # print(c)