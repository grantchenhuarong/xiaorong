import json
from template import PROMPT_TEMPLATE, USER_QUESTION_TEMPLATE, ASSISTANT_ANSWER_TEMPLATE, NO_ANSWER

file_name1 = r"D:\temp\data\cail_data.json"

def uniform(file):
    json_dialogs = []
    with open(file, "r", encoding="utf-8") as f:
        examples = json.load(f)["data"]
        print(type(examples))
        print(len(examples))
        print(examples[0])
        for example in examples:
            paragraphs = example["paragraphs"]

            # 处理场景
            context = paragraphs[0]["context"]

            # 计算问答对数量
            question_list = paragraphs[0]["qas"]
            question_cnt = len(question_list)

            # 循环处理问答
            instruction, output = "", ""
            for i in range(question_cnt):
                # 获取问题
                question = question_list[i]["question"]
                if i == 0:
                    instruction = PROMPT_TEMPLATE.format(context=context, question=question)
                else:
                    instruction += USER_QUESTION_TEMPLATE.format(question=question)

                # 获取回答
                answer = question_list[i]["answers"][0].get("text", NO_ANSWER) \
                    if question_list[i]["answers"] else NO_ANSWER
                answer_concat = ASSISTANT_ANSWER_TEMPLATE.format(answer=answer)

                # 构造 instruction
                if (i < question_cnt - 1):
                    instruction += answer_concat
                else:
                    # 构造 output
                    output = answer

            json_dialogs.append({"instruction": instruction, "input": "", "output": output})

    return json_dialogs

if __name__ == "__main__":
    json_dialogs = uniform(file_name1)
    json.dump(json_dialogs, open("./json/json_dialogs_cail.json", 'w', encoding='UTF-8'), ensure_ascii=False, indent=2)