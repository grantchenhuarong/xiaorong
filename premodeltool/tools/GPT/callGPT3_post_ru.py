import json
import random

import requests

import argparse
from utils import print_args, saveNewContent
import time
import sys
sys.path.append("../../../data_uniform")
from autotestllm.utils import get_usecases, save_to_excel

def getGPTAnswer(url, HEADERS, payload, question):
    answer = ""
    try:
        payload['messages'][0]['content'] = question
        resp=requests.post(url, headers=HEADERS, data=json.dumps(payload))
        json_resp = json.loads(resp.text)
        # print(json_resp)
        if json_resp['err_type'] == None:
            answer = json_resp['msg']['choices'][0]['message']['content']
            # print(answer)
        else:
            answer = ""
            print(json_resp)
    except Exception as e:
        print("getGPTAnswer Exception: ", str(e))
    finally:
        return answer


if __name__ == "__main__":
    # 服务启动参数，为模型加载定义相关变量，为API指定IP、端口
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", type=str, default="config.json")
    parser.add_argument("--output_dir", type=str, default="../autotestllm/report/chatgpt")

    args = parser.parse_args()
    print_args(args)

    config = json.load(open(args.config_file, "r", encoding="utf8"))
    # print(config)

    url = config['aigc_apiurl']
    HEADERS = config['headers']
    payload = {
        "stream": False,
        "model": "gpt-4",
        "temperature": 1,
        "messages": [
            {"role": "user", "content": ""},
        ]
    }

    question = """
    请你扮演一个文学创作大师，按照如下要求完成相关工作：
    1、以{domain}领域的内容随机生成主题作为title，编写创作300字以上的文章作为content
    2、针对上述创作的文章内容，请你提炼出一个相关的问题作为question
    3、对提出的问题进行回答作为answer，要求回答内容只使用文章当中出现过的内容，不创作添加其它任何新内容。如果文章内容无法得到合适问题答案，可以回复“根据文章内容无法有效回答”。

    最后以JSON格式返回该结果，结构要求如下：
    {"标题": title, "文章":content, "问题": question, "回答": answer}"""

    try:
        usecases_cnt = 50

        while True:
            # 获取当前时间的时间戳
            T1 = time.time()
            print("处理开始：")

            answers_list = []
            for i in range(usecases_cnt):
                row_idx = str(i + 1).zfill(3)
                new_question = question.replace("{domain}", random.choice(config['domains']))
                # print(new_question)
                new_content = getGPTAnswer(url, HEADERS, payload, question=new_question)
                answers_list.append((row_idx, "", new_content))
                print(new_content)
                print("处理完成 {0}/{1}".format(i+1, usecases_cnt))
                time.sleep(random.randint(1, 3))

            # 将时间戳转换为本地时间的struct_time对象
            local_time = time.localtime(T1)
            # 使用strftime()方法将struct_time对象格式化为指定的时间字符串
            current_time = time.strftime("%Y%m%d%H%M", local_time)
            # 输出当前的年月日时分
            print(current_time)

            # 所有用例处理完成后，将测试记录内容转储到EXCEL文件，返回前述步骤找到尚未测试的最小权重循环处理
            save_to_excel(answers_list, "chatgpt_ru" + current_time, args.output_dir)

            T2 = time.time()
            print('全部处理完成时间:%s毫秒' % ((T2 - T1) * 1000))

    except Exception as e:
        print("调用ChatGPT异常：", str(e))
    finally:
        pass
