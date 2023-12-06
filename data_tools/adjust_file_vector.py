import copy
import re


'''
const { readFileSync, writeFileSync } = require("fs");

const raw = readFileSync("./hp.txt", "utf-8")
  .split("\n")
  .map((line) => line.replace(/。/g, "。\n").split("\n"))
  .flat()
  .join("\n")
  .replace(/“([\S]+?)”/g, (match) => match.replace(/\n/g, ""))
  .replace(/“([\S\r\n]+?)”/g, (match) => match.replace(/[\r\n]/g, ""))
  .split("\n")
  .map((line) => line.replace(/s/g, "").trim().replace(/s/g, "—"))
  .filter((line) => line)
  .join("\n");

writeFileSync("./ready.txt", raw);
'''


def adjust(src_file, des_file):
    # 读取文件内容
    with open(src_file, 'r', encoding='utf-8') as file:
        content = file.read()

    content = content.split("\n")
    content = [line.replace("。", "。\n").split("\n") for line in content]

    # 将嵌套的列表"flatten"，即变为平铺的一维列表
    content = [item for sublist in content for item in sublist]

    content = "\n".join(content)
    content = re.sub(r'"([^\n]+?)"', lambda x: x.group(0).replace('\n', ''), content)
    content = re.sub(r'"([^\r\n]+?)"', lambda x: x.group(0).replace('\r\n', ''), content)
    content = content.split("\n")
    content = [re.sub('s', '', line.strip()).replace('s', '—') for line in content if line.strip()]

    content = "\n".join(content)

    # 写入文件
    with open(des_file, 'w', encoding='utf-8') as file:
        file.write(content)

def split_text1(src_file, des_file, sentence_size=100):
    # 读取文件内容
    with open(src_file, 'r', encoding='utf-8') as file:
        text = file.read().replace("\n", "")

    text = re.sub(r'([;；.!?。！？\?])([^”’])', r"\1\n\2", text)  # 单字符断句符
    text = re.sub(r'(\.{6})([^"’”」』])', r"\1\n\2", text)  # 英文省略号
    text = re.sub(r'(\…{2})([^"’”」』])', r"\1\n\2", text)  # 中文省略号
    text = re.sub(r'([;；!?。！？\?]["’”」』]{0,2})([^;；!?，。！？\?])', r'\1\n\2', text)

    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    text = text.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    ls = [i for i in text.split("\n") if i]
    for ele in ls:
        if len(ele) > sentence_size:
            ele1 = re.sub(r'([,，.]["’”」』]{0,2})([^,，.])', r'\1\n\2', ele)
            ele1_ls = ele1.split("\n")
            for ele_ele1 in ele1_ls:
                if len(ele_ele1) > sentence_size:
                    ele_ele2 = re.sub(r'([\n]{1,}| {2,}["’”」』]{0,2})([^\s])', r'\1\n\2', ele_ele1)
                    ele2_ls = ele_ele2.split("\n")
                    for ele_ele2 in ele2_ls:
                        if len(ele_ele2) > sentence_size:
                            ele_ele3 = re.sub('( ["’”」』]{0,2})([^ ])', r'\1\n\2', ele_ele2)
                            ele2_id = ele2_ls.index(ele_ele2)
                            ele2_ls = ele2_ls[:ele2_id] + [i for i in ele_ele3.split("\n") if i] + ele2_ls[
                                                                                                   ele2_id + 1:]
                    ele_id = ele1_ls.index(ele_ele1)
                    ele1_ls = ele1_ls[:ele_id] + [i for i in ele2_ls if i] + ele1_ls[ele_id + 1:]

            id = ls.index(ele)
            ls = ls[:id] + [i for i in ele1_ls if i] + ls[id + 1:]

    ls = "\n".join(ls)

    # 写入文件
    with open(des_file, 'w', encoding='utf-8') as file:
        file.write(ls)


def split_text2(src_file, des_file, sentence_size=100, min_sentence_size=50):
    # 读取文件内容
    with open(src_file, 'r', encoding='utf-8') as file:
        text = file.read().replace("\r", "").replace("\n", "")

    text = re.sub(r'([;；.!?。！？\?])([^”’])', r"\1\n\2", text)  # 单字符断句符
    text = re.sub(r'(\.{6})([^"’”」』])', r"\1\n\2", text)  # 英文省略号
    text = re.sub(r'(\…{2})([^"’”」』])', r"\1\n\2", text)  # 中文省略号
    text = re.sub(r'([!?。！？\?]["’”」』]{0,2})([^;；!?，。！？\?])', r'\1\n\2', text)

    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    text = text.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    ls = [i for i in text.split("\n") if i]
    for ele in ls:
        if len(ele) > sentence_size:
            ele1 = re.sub(r'([,，.]["’”」』]{0,2})([^,，.])', r'\1\n\2', ele)
            ele1_ls = ele1.split("\n")
            for ele_ele1 in ele1_ls:
                if len(ele_ele1) > sentence_size:
                    ele_ele2 = re.sub(r'([\n]{1,}| {2,}["’”」』]{0,2})([^\s])', r'\1\n\2', ele_ele1)
                    ele2_ls = ele_ele2.split("\n")
                    for ele_ele2 in ele2_ls:
                        if len(ele_ele2) > sentence_size:
                            ele_ele3 = re.sub('( ["’”」』]{0,2})([^ ])', r'\1\n\2', ele_ele2)
                            ele2_id = ele2_ls.index(ele_ele2)
                            ele2_ls = ele2_ls[:ele2_id] + [i for i in ele_ele3.split("\n") if i] + ele2_ls[
                                                                                                   ele2_id + 1:]
                    ele_id = ele1_ls.index(ele_ele1)
                    ele1_ls = ele1_ls[:ele_id] + [i for i in ele2_ls if i] + ele1_ls[ele_id + 1:]

            id = ls.index(ele)
            ls = ls[:id] + [i for i in ele1_ls if i] + ls[id + 1:]

    #补长向量，将短向量拼接起来
    cnt = len(ls)
    temp_line = ""
    ls2 = []
    for i in range(cnt):
        temp_line += ls[i]
        print(i, ls[i], temp_line)
        if len(temp_line) > min_sentence_size:
            ls2.append(temp_line.lstrip().rstrip())
            temp_line = ""
    if len(temp_line) > 0:
        ls2.append(temp_line.lstrip().rstrip())


    ls2 = "\n".join(ls2)

    # 写入文件
    with open(des_file, 'w', encoding='utf-8') as file:
        file.write(ls2)


if __name__=="__main__":
    split_text2("d:\\temp\\data\\test.txt", "./ready1.txt")