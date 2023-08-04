from __future__ import unicode_literals
import codecs
import json
from template import PROMPT_TEMPLATE, USER_QUESTION_MOSS_TEMPLATE, NO_ANSWER

file_name1 = r"D:\temp\data\cail_data.json"
file_name2 = r"D:\temp\data\cmrc_data.json"
file_name3 = r"D:\temp\data\drcd_data.json"
file_name4 = r"D:\temp\data\dureader_data.json"
file_name5 = r"D:\temp\data\medicine_data.json"
file_name6 = r"D:\temp\data\military_data.json"
file_name7 = r"D:\temp\data\squad_data.json"
file_name8 = r"D:\temp\data\webqa_data.json"
file_name9 = r"D:\temp\data\yiqing_data.json"

def uniform(file):
    json_dialogs = []
    with open(file, "r", encoding="utf-8") as f:
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

                # 循环处理问答
                conversation = []
                human, assistant = "", ""
                for i in range(question_cnt):
                    # 获取问题
                    question = question_list[i]["question"]
                    if i == 0:
                        human = PROMPT_TEMPLATE.format(context=context, question=question)
                    else:
                        human = USER_QUESTION_MOSS_TEMPLATE.format(question=question)

                    # 获取回答
                    assistant = question_list[i]["answers"][0].get("text", NO_ANSWER) \
                        if question_list[i]["answers"] else NO_ANSWER

                    # 构造 conversation
                    conversation.append({"human": human, "assistant": assistant})

                # 控制输入不要超长，这个会引起训练当中GPU卡死、爆显存的问题，如果训练框架没有进行裁剪的话。
                json_dialogs.append({"conversation_id": cnt+1, "category": file.split("\\")[-1].split(".")[0], "conversation": conversation, "dataset": "moss"})

            except Exception as e:
                print(str(e), example)

    return json_dialogs


def jsonl_create(json_dialog_list, file_name):
    with codecs.open(file_name, 'w', encoding='utf-8') as f:
        for dialog in json_dialog_list:
            dict_str = json.dumps(dialog, ensure_ascii=False)
            f.write(dict_str + "\n")

if __name__ == "__main__":
    json_dialogs1 = uniform(file_name1)
    jsonl_create(json_dialogs1, "./json_moss/json_dialogs_cail.jsonl")

    json_dialogs2 = uniform(file_name2)
    jsonl_create(json_dialogs2, "./json_moss/json_dialogs_cmrc.jsonl")

    json_dialogs3 = uniform(file_name3)
    jsonl_create(json_dialogs3, "./json_moss/json_dialogs_drcd.jsonl")

    json_dialogs4 = uniform(file_name4)
    jsonl_create(json_dialogs4, "./json_moss/json_dialogs_dureader.jsonl")

    json_dialogs5 = uniform(file_name5)
    jsonl_create(json_dialogs5, "./json_moss/json_dialogs_medicine.jsonl")

    json_dialogs6 = uniform(file_name6)
    jsonl_create(json_dialogs6, "./json_moss/json_dialogs_military.jsonl")

    json_dialogs7 = uniform(file_name7)
    jsonl_create(json_dialogs7, "./json_moss/json_dialogs_squad.jsonl")

    json_dialogs8 = uniform(file_name8)
    jsonl_create(json_dialogs8, "./json_moss/json_dialogs_webqa.jsonl")

    json_dialogs9 = uniform(file_name9)
    jsonl_create(json_dialogs9, "./json_moss/json_dialogs_yiqing.jsonl")

    json_dialogs = json_dialogs1 + json_dialogs2 + json_dialogs3 + json_dialogs4 + json_dialogs5 + json_dialogs6 + \
                   json_dialogs7 + json_dialogs8 + json_dialogs9
    jsonl_create(json_dialogs, "./json_moss/json_dialogs_moss_ru.jsonl")
