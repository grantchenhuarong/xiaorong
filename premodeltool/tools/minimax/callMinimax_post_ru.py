import json
import random

import requests
import sys
sys.path.append("..")
import argparse
import time
import sys
sys.path.append("../../../data_uniform")
from utils import print_args, get_usecases, save_to_excel


# for testing account
#group_id="1689566671156975"
#api_key="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJOYW1lIjoi5bm_5Lic55yB55S15L-h6KeE5YiS6K6-6K6h6ZmiIiwiU3ViamVjdElEIjoiMTY5Mzk2OTA1NDQ1NDc0NCIsIlBob25lIjoiIiwiR3JvdXBJRCI6IjE2ODk1NjY2NzExNTY5NzUiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiIiLCJDcmVhdGVUaW1lIjoiMjAyMy0wOS0wNiAxMDo1NzozNCIsImlzcyI6Im1pbmltYXgifQ.ER_UY7j-zdf-RRKw_cHqDcS1UaTtYKPkaxTr0f9a5CNhrYLJsKgIaLLXDxlADcHvykZP0OxP2Hlm8BGZm6KYZkkMSsVEVz_GOW4Yv80ZnHTfOt9x91IjOjoftgHQ1W_74mBNo0oHH7ggfKS_C-z1w94WYAOX9X8WXb53yzjRiHwIDL2KSYNYeWJUxLdWOQDaDiQ9Md4RS-9gI41dXgWh2lGDfuI1SE6Q9enQUXXh4l7pCutdOgjQ42Lo3LoKJK40qsZswFDa9L3xSQTwD-sQhrJDoHuZnqfoKdEfO1bezXRoFmEoKml2sQs23k96vfuKnb_30RRQYxMcL8peppuvlw"


group_id="1693897634048370"
api_key="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJOYW1lIjoidGVzdF9jaHJfa2V5IiwiU3ViamVjdElEIjoiMTY5Mzg5NzYzNDc1OTkyMiIsIlBob25lIjoiTVRNMk1UQXhNakF6TURJPSIsIkdyb3VwSUQiOiIxNjkzODk3NjM0MDQ4MzcwIiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiY2hlbmh1YXJvbmdAZ3BkaS5jb20iLCJDcmVhdGVUaW1lIjoiMjAyMy0wOS0wNSAxNTo0MDowNiIsImlzcyI6Im1pbmltYXgifQ.s8hspK0Lh3-GO-24nXK8DU7DAKUxrVreJLR_nINQDDvm2c9e9Ubj4BZMkZdd_RDi70hX4f9SdHhNsAQpSp4glsu6NfY3N1vDpp9m-RjCH8KGlj4R54ksMtCPaccG1sPPKbecl1Yc87tgGr_2TxcpUzwyNAv7zPtT_QUEMGoRHgn8SUMaeQpJUeJ5jGMb9lb6lRud7L9hXk_jWzQF9aH6UAQo2Oh5ZnRu1PFa03PEEZOgnhrfqcCAvcZAsbFW3raQJbgniG8gsb4SwZUIN3u47V79B4ZiWE9w3Kd-ju-DQ0xpX1exIsllzR_9gDybinUmDifsbvb5ThRsKO4D3P6qYg"
url = "https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId=" + group_id

# temperature 当做回答时，设置为 0.01 要求精确的回复；用作创作时，需要设置高一些，如大于1，不然就重复生成类似的内容了。

payload = {
    "bot_setting": [
        {
            "bot_name": "MM智能助理",
            "content": "MM智能助理是一款由MiniMax自研的，没有调用其他产品的接口的大型语言模型。MiniMax是一家中国科技公司，一直致力于进行大模型相关的研究。",
        }
    ],
    "messages": [{"sender_type": "USER", "sender_name": "小明", "text": "帮我用英文翻译下面这句话：我是谁"}],
    "reply_constraints": {"sender_type": "BOT", "sender_name": "MM智能助理"},
    "model": "abab5.5-chat",
    "tokens_to_generate": 2048,
    "temperature": 1.0,
    "top_p": 0.95,
}

headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}

def ask_minimax(url, headers, payload, question):
    text = ""
    try:
        payload["messages"][0]["text"] = question
        response = requests.request("POST", url, headers=headers, json=payload)
        status_code = response.status_code
        # print(status_code)
        # print(type(response.text))
        # print(response.text)
        if status_code == 200:
            text = json.loads(response.text)["reply"]
            # print(text)
    except Exception as e:
        print("ask_minimax exception :", str(e))
    finally:
        return text


if __name__ == "__main__":
    # 服务启动参数，为模型加载定义相关变量，为API指定IP、端口
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", type=str, default="../config.json")
    parser.add_argument("--output_dir", type=str, default="../../datas/minimax")

    args = parser.parse_args()
    print_args(args)

    config = json.load(open(args.config_file, "r", encoding="utf8"))
    # print(config)


    question = """
    请你扮演一个文学创作大师，按照如下要求完成相关工作：
    1、以{domain}领域的内容随机生成主题作为title，编写创作300字以上的文章作为content
    2、针对上述创作的文章内容，请你提炼出一个相关的问题作为question
    3、对提出的问题进行回答作为answer，要求回答内容只使用文章当中出现过的内容，不创作添加其它任何新内容。如果文章内容无法得到合适问题答案，可以回复“根据文章内容无法有效回答”。

    最后以JSON格式返回该结果，结构要求如下：
    {"标题": title, "文章":content, "问题": question, "回答": answer}"""

    try:
        usecases_cnt = 30

        while True:
            # 获取当前时间的时间戳
            T1 = time.time()
            print("处理开始：")

            answers_list = []
            for i in range(usecases_cnt):
                row_idx = str(i + 1).zfill(3)
                domain = random.choice(config['adjectives'])+"事件"
                new_question = question.replace("{domain}", domain)
                print(new_question)
                new_content = ask_minimax(url, headers, payload, question=new_question)
                print(new_content)
                if(len(new_content)>100):
                    answers_list.append((row_idx, domain, new_content))
                print("处理完成 {0}/{1}".format(i+1, usecases_cnt))
                time.sleep(random.randint(3, 5))

            # 将时间戳转换为本地时间的struct_time对象
            local_time = time.localtime(T1)
            # 使用strftime()方法将struct_time对象格式化为指定的时间字符串
            current_time = time.strftime("%Y%m%d%H%M", local_time)
            # 输出当前的年月日时分
            print(current_time)

            # 所有用例处理完成后，将测试记录内容转储到EXCEL文件，返回前述步骤找到尚未测试的最小权重循环处理
            save_to_excel(answers_list, "minimax_ru" + current_time, args.output_dir)

            T2 = time.time()
            print('全部处理完成时间:%s毫秒' % ((T2 - T1) * 1000))
            time.sleep(random.randint(10, 30))
    except Exception as e:
        print("调用Minimax平台API异常：", str(e))
    finally:
        pass
