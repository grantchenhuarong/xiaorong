#!/bin/bash
import pandas as pd
import json
import codecs

data_file = "../premodeltool/datas/minimax/summary/minimax_good_samples20231007.xlsx"

def get_samples(file):
    samples_list = []
    df = pd.read_excel(file)
    samples_list = df['回复'].tolist()
    return samples_list


# PROMPT_TEMPLATE="""已知信息：\n\n{0}\n
# 从上述已知信息，选择内容来回答用户的问题，不能添加已知信息之外的内容。如果无法从中得到答案，请回答 “根据已知信息无法回答该问题”。\n
# 问题是：{1}\n
# 答案是： """

PROMPT_TEMPLATE = """<指令>根据已知信息，简洁和专业的来回答问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题”，不允许在答案中添加编造成分，答案请使用中文。 </指令>

<已知信息>{0}</已知信息>

<问题>{1}</问题>"""

def construct_datas(samples_list):
    data_list = []
    for sample in samples_list:
        try:
            data = json.loads(sample)
            # title = data['标题']
            article = data['文章']
            question = data['问题']
            answer = data['回答']
            instruction = PROMPT_TEMPLATE.format(article, question)
            data_list.append({"instruction": instruction, "input": "", "output": answer})

        except Exception as e:
            print("construct_datas excp: ", str(e), sample)

    return data_list


def write_json_file(data_list, output_file):
    json.dump(data_list, open(output_file, 'w', encoding='UTF-8'), ensure_ascii=False, indent=2)


def jsonl_create(json_dialog_list, file_name):
    with codecs.open(file_name, 'w', encoding='utf-8') as f:
        for dialog in json_dialog_list:
            dict_str = json.dumps(dialog, ensure_ascii=False)
            f.write(dict_str + "\n")


if __name__ == "__main__":
    samples_list = get_samples(data_file)
    print(len(samples_list))

    data_list = construct_datas(samples_list)
    print(len(data_list))

    # jsonl_create(data_list, "./json/minimax_ru_good_samples.jsonl")
    write_json_file(data_list, "./json/minimax_good_samples20231007.json")