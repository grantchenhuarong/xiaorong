import json
import random

import requests

import pandas
import argparse
from utils import print_args, saveNewContent
import time

def getGPTAnswer(url, HEADERS, payload, question):
    answer = ""
    try:
        payload['messages'][config['question_idx']]['content'] = question
        resp=requests.post(url, headers=HEADERS, data=json.dumps(payload))
        json_resp = json.loads(resp.text)
        # print(json_resp)
        if json_resp['err_type'] == None:
            answer = json_resp['msg']['choices'][0]['message']['content']
            # print(answer)
    except Exception as e:
        print("getGPTAnswer Exception: ", str(e))
    finally:
        return answer


if __name__ == "__main__":
    # 服务启动参数，为模型加载定义相关变量，为API指定IP、端口
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", type=str, default="config.json")
    parser.add_argument("--input_excel", type=str,default="./datas/new0605.xlsx")
    parser.add_argument("--sheet_name", type=str, default="Sheet")
    parser.add_argument("--col_idx", type=str, default=0)
    parser.add_argument("--output_excel", type=str, default="./datas/chatgpt_resp.xlsx")

    args = parser.parse_args()
    print_args(args)

    config = json.load(open(args.config_file, "r", encoding="utf8"))
    # print(config)

    url = config['aigc_apiurl']
    HEADERS = config['headers']
    payload = {
        "stream": False,
        "model": "gpt-3.5-turbo",
        "temperature": 1,
        "messages": [
            {"role": "system", "content": config['chat_actor']},
            {"role": "user", "content": config['prefix_modal']},
            {"role": "assistant", "content": config['chat_transition']},
            {"role": "user", "content": ""}
        ]
    }

    question = """机器人提问:！！您好，我是大塘街社区卫生服务中心的智能助手，;请问您是吴传秉本人或他家属吗
    居民回复:是的。
    机器人提问:我中心现举办一年一度的国家免费老年人健康体检，65岁及以上老年人都可参加，（仅限2023年未参加过体检的人群）。现诚邀您参加体检，时间是：逢周二至周五（节假日除外），上午：8:00-10:00，体检地址是：德政中路拾桂坊16号，，请问您愿意参加吗
    居民回复:吴传秉，他现在行动不方便。
    机器人提问:好的，感谢您的接听，祝您身体健康、生活愉快，再见！
    居民回复:Hm.#####\n结论：[MASK]\n原因：[MASK]"""

    try:
        T1 = time.time()
        print("处理开始：" )

        df = pandas.read_excel(args.input_excel, sheet_name=args.sheet_name, usecols=[int(args.col_idx)], header=None)
        counter = 0
        old_new_paragraphs = []
        while counter < df.size:  # series-> numpy.ndarray -> list[str] -> str
            question = df.iloc[counter].values[0]
            question = config['prefix_modal'] + question + config['suffix_modal']
            # print(question)

            new_content = getGPTAnswer(url, HEADERS, payload, question)
            print("new_content--", new_content)

            old_new_paragraphs.append((df.iloc[counter].values[0], new_content))

            counter += 1
            print("处理完成 {0}/{1}".format(counter, df.size))

            time.sleep(random.randint(1, 3))

        # 输出到指定EXCEL文件当中
        saveNewContent(old_new_paragraphs, args.output_excel, 0)

        T2 = time.time()
        print('全部处理完成时间:%s毫秒' % ((T2 - T1) * 1000))

    except Exception as e:
        print("使用哈工大HLP识别人名异常：", str(e))
    finally:
        pass
