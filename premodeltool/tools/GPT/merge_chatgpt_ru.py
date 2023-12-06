# !/bin/bash

import pandas as pd
import os
import sys
sys.path.append("..")
from utils import save_to_excel, check_valid_columns_count

chatgpt_ru_samples_dir = "..\..\datas\chatgpt" # 定义 chatgpt 阅读理解文件的所在目录
chatgpt_ru_samples_file_prefix = "chatgpt_ru"  # 定义 chatgpt 阅读理解文件前缀
dicts = ["标题", "文章", "问题", "回答"] # 必备的内容
check_columns = len(dicts) # 必备的检查项
end_delimiters = "\"}" # 结束符号
minimun_len = 2 # 每列内容最短长度

EXCEPTION_LACK_OF_COMMA = "Expecting ',' delimiter:"
lack_of_comma_key_words = ["\"问题\":", "\"回答\":"]


#补全后边两个关键字前面缺少逗号分割符的错误情况
import copy
def fix_exception_lack_of_comma(content):
    new_content = copy.deepcopy(content)
    for key_word in lack_of_comma_key_words:
        pos = new_content.find(key_word)
        if pos > -1: # 由关键字回溯找到第一个单引号结束符，判断这中间是否存在逗号
            pos -= 1
            while pos > 0 and new_content[pos] != "\"":
                if new_content[pos] == "," or new_content[pos] == "，":
                    break
                else:
                    pos -= 1
        if new_content[pos] == "\"": # 缺少逗号，则进行插入操作
            new_content = new_content[0:pos+1] + "," + new_content[pos+1:]
        elif new_content[pos] == "，": # 中文逗号要改成英文
            new_content = new_content[0:pos] + "," + new_content[pos+1:]

    return new_content

# 定义一个函数，读取单个文件，返回完好的JSON回复数据列表，以及检查不完好的回复数据列表
def get_single_excel_records(excel_file_name):
    list_good_json_records, list_bad_json_records = [], []

    try:
        # 读取相应的excel文件
        df = pd.read_excel(excel_file_name).replace("\r\n", "")
        series = df['序号'].tolist()
        types = df['问题'].tolist()
        samples = df['回复'].tolist()

        # 循环检查每一行数据
        for (serie, type, sample) in zip(series, types, samples):
            if len(sample) >= minimun_len:
                try:
                    # 检查前后是否有字典括号{}优先补充
                    content = sample.strip().replace("\n", "")
                    print(str(serie), content[0], content[-1])

                    ## 应对 Extra data: line 1 column 404 (char 403)
                    # 定位最右边的结束符号 "}，如果不是且中间有结束符，考虑强行截断
                    if content[-len(end_delimiters)] != end_delimiters:
                        end_pos = content.rfind(end_delimiters)
                        if end_pos != -1:
                            total_len = len(content)
                            if end_pos + 2 != total_len:
                                content = content[0: end_pos + 1]

                    # Expecting ',' delimiter: 。""，需要替换成为 ," 有点风险，会不会将内容替换掉？
                    content = content.replace("。\"\"", "。\",\"")
                    content = content.replace("\"\"回答\":\"", "\",\"回答\":\"")
                    content = content.replace("\" \"回答\": \"", "\",\"回答\":\"")
                    content = content.replace("\"\"问题\":\"", "\",\"问题\":\"")
                    content = content.replace("\" \"问题\": \"", "\",\"问题\":\"")

                    if content[0] != '{':
                        content = "{" + content
                    if content[-1] != '}':
                        content = content + "}"

                    # 循环检查每列的内容是否具备
                    valid_counts, excp_result = check_valid_columns_count(dicts, content, minimun_len)
                    #  "问题":  "回答": 生成前面缺少逗号 ,
                    if excp_result.startswith(EXCEPTION_LACK_OF_COMMA):
                        content = fix_exception_lack_of_comma(content)
                        valid_counts, excp_result = check_valid_columns_count(dicts, content, minimun_len)
                        if (len(excp_result) == 0):
                            print("已修复")

                    # Unterminated string starting at:  抛弃掉
                    # Expecting ':' delimiter:

                    # 全部OK则打入返回的好数列，有不足列则打入返回的坏数列
                    if valid_counts == check_columns:
                        list_good_json_records.append((serie, type, content))
                    else:
                        list_bad_json_records.append((serie, type, content))
                except Exception as e:
                    result = str(e)
                    print(str(serie), "get_single_excel_records exception: ", result, content)

    except Exception as e:
        print("get_single_excel_records exception:{}====={}".format( str(e), excel_file_name))
    finally:
        return list_good_json_records, list_bad_json_records


# 定义一个函数，汇总目录下所有文件完好JSON回复数据列表，以及检查不完好的回复数据列表
def merge_all_records(dir_path, pre_fix):
    # 获取结果文件列表
    results = os.listdir(dir_path)
    if len(results) > 0:
        results = list(filter(lambda x: x.startswith(pre_fix), results))
    return results

# 约束及局限： 相关的数据量能够在内存当中完整处理，目前处理能力在10^3数量级，可以充分


if __name__ == "__main__":
    # file_name = "../autotestllm/report/chatgpt/chatgpt_ru202309080750.xlsx"
    # list_good_json_records, list_bad_json_records = get_single_excel_records(file_name)
    # print("好数据列表：", list_good_json_records)
    # print("坏数据列表：", list_bad_json_records)

    # 测试逗号补全
#     content = """
# {"标题": "探索物理领域中的时间本质", "文章": "在物理学中，时间被视为描述物质存在的四维空间之一。时间概念在许多理论中得到了广泛应用，如相对论、量子力学和宇宙学。尽管时间具有普遍性，但其本质和起源仍然备受争议。
#
# 在相对论中，爱因斯坦提出时间可以作为一种可塑的量，其流速因观察者和物体所处位置不同而变化。这一观点挑战了传统观念，认为时间是绝对的、均匀流逝的。然而，相对论的时间概念与实际观测结果相符，并为理解引力和时空的性质提供了重要基础。
#
# 在量子力学中，时间概念变得更加复杂。在亚原子尺度上，粒子表现出一种被称为量子态的奇特行为，这导致时间概念的不确定性。一些理论认为，时间可能并不是一个基本量，而是由更基本的实体构成。
#
# 宇宙学则为我们提供了研究时间起源的机会。大爆炸理论认为，宇宙起源于一个高温、高密度的状态，随后逐渐膨胀形成我们今天所看到的宇宙。在这个过程中，时间和空间一同诞生，并由此引发了对时间本质的探索。
#
# 尽管物理学家们提出了各种时间概念和理论，但其本质仍然没有定论。新的实验和观测结果可能为我们提供新的线索，以进一步理解时间的本质。"
#    "问题": "在物理学中，时间是如何被视为描述物质存在的四维空间之一的？", "回答": "在物理学中，时间被视为描述物质存在的四维空间之一，与其他三个空间维度一起构成了我们所知的宇宙。这种观念在不同理论中得到了广泛应用，如相对论、量子力学和宇宙学。"
# }    """
#
#     new_content = fix_exception_lack_of_comma(content)
#     print(new_content)

    sample_files = merge_all_records(chatgpt_ru_samples_dir, chatgpt_ru_samples_file_prefix)
    total_list_good_json_records, total_list_bad_json_records = [], []

    for sample_file in sample_files:
        print(sample_file)
        list_good_json_records, list_bad_json_records = \
            get_single_excel_records(chatgpt_ru_samples_dir + "/" + sample_file)

        total_list_good_json_records += list_good_json_records
        total_list_bad_json_records += list_bad_json_records

    save_to_excel(total_list_good_json_records, "chatgpt_good_samples", "..\..\datas\chatgpt\summary")
    save_to_excel(total_list_bad_json_records, "chatgpt_bad_samples", "..\..\datas\chatgpt\summary")