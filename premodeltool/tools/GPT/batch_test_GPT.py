##  https://api.minimax.chat/document/guides/chat-pro?id=64b79fa3e74cddc5215939f4

import time
import random
import sys
import json
sys.path.append("..")
from utils import print_args, get_usecases, save_to_excel
import argparse
import copy
from common import streamGetGPTAnswer


if __name__ == "__main__":
    # 服务启动参数，为模型加载定义相关变量，为API指定IP、端口
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", type=str, default="../config.json")

    args = parser.parse_args()
    print_args(args)

    config = json.load(open(args.config_file, "r", encoding="utf8"))
    # print(config)

    url = config['aigc_apiurl']
    HEADERS = config['headers']
    payload = {
        "stream": True,
        "model": "gpt-3.5-turbo",
        "temperature": 0.01,
        "messages": [
            {"role": "user", "content": ""},
        ]
    }
# GPT4: "gpt-4"

    # 读出用例文件中问题进入数组
    usecases_file = r"../../datas/usecases/reading_undestanding.xlsx"
    use_cases_list = get_usecases(usecases_file)[485:486]
    print("first_record: ", use_cases_list[0])
    print("用例数量：", len(use_cases_list))
    answers_list = []
    for i in range(len(use_cases_list)):
        row_idx = str(i + 1).zfill(3)
        question = use_cases_list[i]
        print("正在请求： ", row_idx, question)
        new_content = streamGetGPTAnswer(url, HEADERS, payload, question)
        print("回复：", new_content)
        answers_list.append((row_idx, question, copy.deepcopy(new_content)))
        time.sleep(random.randint(1, 3))

    # # 所有用例处理完成后，将测试记录内容转储到EXCEL文件，返回前述步骤找到尚未测试的最小权重循环处理
    # client_test_result_dir = r"report"
    # save_to_excel(answers_list, "gpt_20230915", client_test_result_dir)