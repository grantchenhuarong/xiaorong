import json
from template import PROMPT_TEMPLATE, USER_QUESTION_TEMPLATE, ASSISTANT_ANSWER_TEMPLATE

file_name1 = r"D:\temp\data\c3\d-dev.json"
file_name2 = r"D:\temp\data\c3\d-train.json"
file_name3 = r"D:\temp\data\c3\m-dev.json"
file_name4 = r"D:\temp\data\c3\m-train.json"


def uniform(file):
    json_dialogs = []
    with open(file, "r", encoding="utf-8") as f:
        examples = json.load(f)
        print(len(examples))
        print(examples[0])
        for example in examples:
            # if len(example) != 3:
            #     print("length of example not equal 3: -------------------", example)
            # if len(example[1]) > 1:
            #     print("question numbers greater than 1: -----------------", example)
            # 处理场景
            context = "\n".join(example[0])

            # 计算问答对数量
            question_cnt = len(example[1])
            # 循环处理问答
            instruction, output = "", ""
            for i in range(question_cnt):
                # 获取问题
                if i == 0:
                    question = example[1][i]['question'] + "可选答案有-" + "，".join(example[1][0]['choice'])
                    instruction = PROMPT_TEMPLATE.format(context=context, question=question)
                else:
                    question = USER_QUESTION_TEMPLATE.format(question=example[1][i]['question'] +
                                     "-可选答案有：" + "，".join(example[1][i]['choice']))
                    # 构造 instruction
                    instruction += question

                # 获取回答
                answer = ASSISTANT_ANSWER_TEMPLATE.format(answer=example[1][i]['answer'])

                # 构造 instruction
                if (i < question_cnt - 1):
                    instruction += answer
                else:
                    # 构造 output
                    output = example[1][i]['answer']

            json_dialogs.append({"instruction": instruction, "input": "", "output": output})
            # print(instruction + output)

    return json_dialogs

if __name__ == "__main__":
    json_dialogs1 = uniform(file_name1)
    json_dialogs2 = uniform(file_name2)
    json_dialogs3 = uniform(file_name3)
    json_dialogs4 = uniform(file_name4)
    json_dialogs = json_dialogs1 + json_dialogs2 + json_dialogs3 + json_dialogs4
    json.dump(json_dialogs, open("./json/json_dialogs_c3.json", 'w', encoding='UTF-8'), ensure_ascii=False, indent=2)