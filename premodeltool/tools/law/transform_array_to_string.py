import json

src_file = "d:\\temp\\data\\disc-law-sft\\DISC-Law-SFT-Triplet-released.jsonl"
des_file = "../../datas/law/DISC-Law-SFT-Triplet.jsonl"

if __name__ == "__main__":
    sft_data = []

    with open(src_file, 'r', encoding='utf-8') as f:
        rows = f.readlines()
        print(len(rows))

        for data in rows:
            json_row = json.loads(data)
            context = "\n请依据如下相关法律条文规定，对上述法律事实进行分析推断。\n"
            for reference in json_row['reference']:
                context += reference
                context += "\n"

            id = json_row['id']
            input = json_row['input']
            output = json_row['output']
            sft_data.append({"id": id, "input": input + context, "output": output})

    if len(sft_data) > 0:
        with open(des_file, 'w', encoding='utf-8') as f:
            for row in sft_data:
                dict_str = json.dumps(row, ensure_ascii=False)
                f.write(dict_str + "\n")