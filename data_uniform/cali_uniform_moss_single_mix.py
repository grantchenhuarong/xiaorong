from __future__ import unicode_literals
import codecs
import random

import json
from template import PROMPT_TEMPLATE_MIXED, NO_ANSWER

file_name1 = r"D:\temp\data\cail_data.json"
file_name2 = r"D:\temp\data\cmrc_data.json"
file_name3 = r"D:\temp\data\drcd_data.json"
file_name4 = r"D:\temp\data\dureader_data.json"
file_name5 = r"D:\temp\data\medicine_data.json"
file_name6 = r"D:\temp\data\military_data.json"
file_name7 = r"D:\temp\data\squad_data.json"
file_name8 = r"D:\temp\data\webqa_data.json"
file_name9 = r"D:\temp\data\yiqing_data.json"
file_name_moss = r"D:\temp\data\moss-003-sft-data.jsonl"
file_name_math = r"D:\temp\data\school_math_0.25M.json"

too_long_cnt = 0

def read_answer(file):
    global too_long_cnt
    json_dialogs = []
    with open(file, 'r', encoding='utf-8') as f:
        examples = json.load(f)["data"]
        print(type(examples))
        print(len(examples))
        examples_cnt = len(examples)
        print(examples[0])
        for cnt in range(examples_cnt):
            example = examples[cnt]
            try:
                paragraphs = example["paragraphs"]

                # 处理场景
                context = paragraphs[0]["context"]

                # 计算问答对数量
                question_list = paragraphs[0]["qas"]
                question_cnt = len(question_list)

                if question_cnt == 1: # 只保留一问一答的场景
                    conversation = []

                    human, assistant = "", ""

                    # 获取问题
                    question = question_list[0]["question"]
                    human = PROMPT_TEMPLATE_MIXED.format(context=context, question=question)

                    # 获取回答在正文位置
                    assistant_answer_pos = question_list[0]["answers"][0].get("answer_start", -1) \
                        if question_list[0]["answers"] else -1

                    if assistant_answer_pos > -1:
                        # 获取回答
                        assistant = question_list[0]["answers"][0].get("text", NO_ANSWER) \
                            if question_list[0]["answers"] else NO_ANSWER
                    else:
                        assistant = NO_ANSWER

                    # 构造 conversation
                    conversation.append({"human": human, "assistant": assistant})
                    if(len(str(conversation))) < 3500:
                        # 控制输入不要超长，这个会引起训练当中GPU卡死、爆显存的问题，如果训练框架没有进行裁剪的话。
                        json_dialogs.append({"conversation_id": cnt+1, "category": file.split("\\")[-1].split(".")[0], "conversation": conversation, "dataset": "moss"})
                    else:
                        too_long_cnt += 1
                        print(str(too_long_cnt) +" Too long!!! ", conversation)
                else:
                    print("=========================", example)
            except Exception as e:
                print(str(e), example)

    return json_dialogs


def jsonl_create(json_dialog_list, file_name):
    with codecs.open(file_name, 'w', encoding='utf-8') as f:
        for dialog in json_dialog_list:
            dict_str = json.dumps(dialog, ensure_ascii=False)
            f.write(dict_str + "\n")


def get_samples(json_dialogs, choice_cnt):
    total_cnt = len(json_dialogs)
    if total_cnt > choice_cnt:
        json_dialogs = random.sample(json_dialogs, choice_cnt)
    return json_dialogs


def get_maths(file_name):
    json_dialogs = []
    with open(file_name, 'r', encoding='utf-8') as f:
        examples = f.readlines()
        examples_cnt = len(examples)
        print(examples[0])
        print(type(examples[0]))
        for cnt in range(examples_cnt):
            try:
                dialog = examples[cnt][1:-2].split(r'", "input": "", ')  ## 去除 '{  }'后，中间用input分段

                conversation = []
                if len(dialog) == 2: # 一问一答
                    # 获取问题
                    question = dialog[0].replace(r'"instruction": "', '')
                    answer = dialog[1].replace(r'"output": "', '')

                    # 构造 conversation
                    conversation.append({"human": question, "assistant": answer})
                    if (len(str(conversation))) < 3500:
                        # 控制输入不要超长，这个会引起训练当中GPU卡死、爆显存的问题，如果训练框架没有进行裁剪的话。
                        json_dialogs.append({"conversation_id": cnt + 1, "category": "math",
                                             "conversation": conversation, "dataset": "belle"})
            except Exception as e:
                print(str(e), dialog)

    return json_dialogs


if __name__ == "__main__":

    # 抽取20万MOSS语料  从百万资料当中抽取会爆内存，改用服务器脚本实施
    # choice_cnt = 10000
    # with open(file_name_moss, 'r', encoding='utf-8') as f:
    #     json_dialogs1 = f.read()
    #     json_dialogs1 = get_samples(json_dialogs1, choice_cnt)

    # 抽取3万特定问答的语料
    json_dialogs6 = read_answer(file_name6)
    jsonl_create(json_dialogs6, "./json_moss/json_dialogs_military.jsonl")

    json_dialogs8 = read_answer(file_name8)
    jsonl_create(json_dialogs8, "./json_moss/json_dialogs_webqa.jsonl")

    json_dialogs9 = read_answer(file_name9)
    jsonl_create(json_dialogs9, "./json_moss/json_dialogs_yiqing.jsonl")

    choice_cnt = 30000
    json_dialogs2 = json_dialogs6 + json_dialogs8 + json_dialogs9
    json_dialogs2 = get_samples(json_dialogs2, choice_cnt)

    # 抽取2万数学计算的语料
    choice_cnt = 20000
    json_dialogs3 = get_maths(file_name_math)
    json_dialogs3 = get_samples(json_dialogs3, choice_cnt)

    # json_dialogs = json_dialogs1 + json_dialogs2 + json_dialogs3
    json_dialogs = json_dialogs2 + json_dialogs3
    random.shuffle(json_dialogs)
    jsonl_create(json_dialogs, "./json_moss/json_dialogs_moss_single_mixed.jsonl")

## shuf -n200000 moss-003-sft-data.jsonl > moss-003-sft-data-200000.jsonl
## cat moss-003-sft-data-200000.jsonl >> json_dialogs_moss_single_mixed.jsonl
## shuf -n250000 json_dialogs_moss_single_mixed.jsonl > json_dialogs_moss_mixed.jsonl
## more json_dialogs_moss_single_mixed.jsonl |wc -l
## rm -rf json_dialogs_moss_single_mixed.jsonl