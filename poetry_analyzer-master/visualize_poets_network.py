import pickle
import argparse
import os
import math
#获取排名前visulize_range的引用关系
def get_concerned_relations_by_range(reference_relations_counter, visulize_range):
  # 获取引用关系
  relations = reference_relations_counter.most_common(visulize_range)
  max_refer_count = relations[0][1]
  min_refer_count = relations[-1][1]

  return relations, max_refer_count, min_refer_count

def generate_html_page(relations, saved_html_file, count_to_plot_threshold = 1):
  html_dir = os.path.dirname(saved_html_file)
  html_head_path = os.path.join('static', 'html_head.txt')
  html_tail_path = os.path.join('static', 'html_tail.txt')
  links_text = 'links: [\n'
  links_item_format = """{source: '%s', target: '%s'
    },
   """
  filtered_authors = set()
  for (refered_by, refered), count in relations:
    #防止产生单独节点
    if refered_by == refered:
      continue
    # 小于门限跳过
    if count < count_to_plot_threshold:
      continue

    filtered_authors.add(refered_by)
    filtered_authors.add(refered)
    count = math.sqrt(count)
    links_text += links_item_format % (refered_by, refered)
  links_text += '],\n'





  #---------------------------------格式化links数据，并写入txt，用于计算NetWork------------------------#
  # links_text_pre = '[\n'
  # links_item_format = "'%s'\n"
  # filtered_authors = set()
  # for (refered_by, refered), count in relations:
  #   #防止产生单独节点
  #   if refered_by == refered:
  #     continue
  #   # 小于门限跳过
  #   if count < count_to_plot_threshold:
  #     continue
  #
  #   filtered_authors.add(refered_by)
  #   filtered_authors.add(refered)
  #   links_text_pre += links_item_format % (refered_by)
  #
  # links_text_pre += ']\n'
  # #============================================
  #
  # links_text_next = '[\n'
  # links_item_format = "'%s'\n"
  # filtered_authors = set()
  # for (refered_by, refered), count in relations:
  #   #防止产生单独节点
  #   if refered_by == refered:
  #     continue
  #   # 小于门限跳过
  #   if count < count_to_plot_threshold:
  #     continue
  #
  #   filtered_authors.add(refered_by)
  #   filtered_authors.add(refered)
  #   links_text_next += links_item_format % (refered)
  #
  # links_text_next += ']\n'
  #
  # # 格式化node数据,并写入txt
  # data_text = '[\n'
  # data_item_format ="'%s'\n"
  # for author in filtered_authors:
  #   data_text += data_item_format % author
  #
  # data_text += ']\n'
  #
  # with open('./static/data_txt', 'w', encoding = 'utf-8') as f:
  #   f.write(data_text)
  # with open('./static/link_txt_pre', 'w', encoding='utf-8') as f:
  #   f.write(links_text_pre)
  # with open('./static/link_txt_next', 'w', encoding='utf-8') as f:
  #   f.write(links_text_next)


#-----------------------------------------计算节点大小-------------------------------
  count_num=[]
  filtered_authors=list(filtered_authors)
  for i in range(len(filtered_authors)):
    counts=0
    for (refered_by,refered),count in relations:
       if(filtered_authors[i]==refered_by or filtered_authors[i]==refered):
          counts+=1;
    count_num.append(counts)

  #格式化node数据
  data_text = 'data:[\n'
  data_item_format = "{name: '%s',value: %d },\n"
  for i in range(len(filtered_authors)):
    data_text += data_item_format % (filtered_authors[i],count_num[i])
  data_text += '],\n'


#———————————————————————————————————————————————————生成HTML——————————————————————————————————————
  #读取html的head和tail部分
  with open(html_head_path, 'r', encoding = 'utf-8') as f:
    head_text = f.read()

  with open(html_tail_path, 'r', encoding = 'utf-8') as f:
    tail_text = f.read()

  #合并存储为html
  with open(saved_html_file, 'w', encoding = 'utf-8') as f:
    f.write(head_text + data_text + links_text + tail_text)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--relations_path', type=str, default='save/reference_relations.pkl',
                      help='file to load relations static')
  parser.add_argument('--data_dir', type=str, default='static',
                      help='directory to load authors file')
  parser.add_argument('--html_dir', type=str, default='templates',
                      help='directory to save templates page')
  args = parser.parse_args()
  with open(args.relations_path, 'rb') as f:
    reference_relations_counter, reference_relations_text = pickle.load(f)
  #生成全唐排名前600的关系图
  relations, max_refer_count, min_refer_count = get_concerned_relations_by_range(reference_relations_counter,600)
  saved_html = os.path.join(args.html_dir, 'full_tang_poets_net.html')
  generate_html_page(relations, saved_html)
if __name__ == '__main__':
        main()
