#! /bin/bash

from autotestglm.utils import save_one_column_to_excel


def extract_by_start_end(content, start_str, end_str):
    pattern_list = []

    try:
        start_str_len = len(start_str)
        start_pos = content.find(start_str, 0)
        while start_pos != -1:
            end_pos = content.find(end_str, start_pos + start_str_len)
            if end_pos != -1:
                pattern_list.append(content[start_pos + start_str_len: end_pos])
            start_pos = content.find(start_str, start_pos + start_str_len)
    except Exception as e:
        print("extract_by_start_end exception: == ", str(e))
    finally:
        return pattern_list


if __name__ == "__main__":

    try:
        with open("../datas/langchain/log_langchain_test.log", mode="r", encoding="utf-8") as f:
            content = f.read()
            pattern_list = extract_by_start_end(content, "__call:", "INFO:")
            for pattern in pattern_list:
                print(pattern)

        save_one_column_to_excel(pattern_list, "langchain", "./datas/langchain")
    except Exception as e:
        print("extract_content_by_pattern: ", str(e))

