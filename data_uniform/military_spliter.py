import json
from template import PROMPT_TEMPLATE, USER_QUESTION_TEMPLATE, ASSISTANT_ANSWER_TEMPLATE, NO_ANSWER

file_name4 = r"./json/json_dialogs_dureader.json"
file_name6 = r"./json/json_dialogs_military.json"

file_name_military1 = r"./json/json_dialogs_military153.json"
# 拆分整数
def split_integer(m, n):
    assert n > 0
    quotient = int(m / n)
    remainder = m % n
    if remainder > 0:
        return [quotient] * (n - remainder) + [quotient + 1] * remainder
    if remainder < 0:
        return [quotient - 1] * -remainder + [quotient] * (n + remainder)
    return [quotient] * n


# 累加整数数组
def accumulate_integer_list(split_list):
    end = 0
    accum_list = [0]
    for pos in split_list:
        end += pos
        accum_list.append(end)
    return accum_list

def spliter(file, parts=5):

    examples = []
    with open(file, "r", encoding="utf-8") as f:
        examples = json.load(f)
        print(type(examples))

    examples_cnt = len(examples)
    print(examples_cnt)
    spliters = split_integer(examples_cnt, parts)
    accum_list = accumulate_integer_list(spliters)
    print(accum_list)

    for i in range(parts):
        json_dialogs = examples[accum_list[i] : accum_list[i+1]]
        new_file = file.replace(".json", str(i+1)+".json")
        print(new_file)
        json.dump(json_dialogs, open(new_file, 'w', encoding='UTF-8'), ensure_ascii=False, indent=2)

if __name__ == "__main__":

    json_dialogs = spliter(file_name_military1)



