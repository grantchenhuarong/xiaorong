# 将cali的法律事实多轮问答，转换成为单轮的问答，以作为SFT训练法律问题的补充材料

import json

src_file = "d:\\temp\\data\\cail_data.json"
des_file = "../../datas/law/DISC_Law_SFT_cail_with_no_answer.jsonl"
if __name__ == "__main__":
    sft_data = []

    with open(src_file, 'r', encoding='utf-8') as f:
        json_content = json.load(f)
        print(len(json_content['data']))

        for data in json_content['data']:
            # if len(data['paragraphs']) > 1:
            #     print(data['id'])
            for paragraph in data['paragraphs']:
                context = paragraph['context']
                for qa in paragraph['qas']:
                    question = qa['question']
                    is_impossible = qa['is_impossible']
                    if not is_impossible:
                        answer = qa['answers'][0]['text']
                    else:
                        answer = "根据上述已经提供的法律事实，无法有效回答该问题。"
                    id = qa['id']
                    # print("{} 请阅读如下法律事实，回答后继问题。{}\n请问：{}\n回答：{}".format(id, context, question, answer))
                    sft_data.append({"id": id, "instruction":"请阅读如下法律事实，回答后继问题。\n",
                                     "input": context + "\n请问：" + question, "output": answer})

    if len(sft_data) > 0:
        with open(des_file, 'w', encoding='utf-8') as f:
            for row in sft_data:
                dict_str = json.dumps(row, ensure_ascii=False)
                f.write(dict_str+"\n")
