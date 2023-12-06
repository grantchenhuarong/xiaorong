import json
import random

src_file = "d:\\temp\\data\\school_math_0.25M.json"
des_file = "../../datas/law/DISC-Law-SFT-Math-50k.jsonl"

if __name__ == "__main__":
    sft_data = []

    with open(src_file, 'r', encoding='utf-8') as f:
        rows = f.readlines()
        print(len(rows))

        random_rows = random.choices(rows, k = 50000)
        for data in random_rows:
            json_row = json.loads(data)
            instruction = "请按照step by step的方式推理解答如下的数学问题。"
            input = json_row['instruction'] + "\n" + json_row['input']
            output = json_row['output']
            sft_data.append({"instruction": instruction, "input": input, "output": output})

    if len(sft_data) > 0:
        with open(des_file, 'w', encoding='utf-8') as f:
            for row in sft_data:
                dict_str = json.dumps(row, ensure_ascii=False)
                f.write(dict_str + "\n")