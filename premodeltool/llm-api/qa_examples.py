#作者：陈华荣
#功能：简单实现一个调用LLM的API服务获取回答的训练程序
#时间：2023年12月04日
#版本： v0.9

import sys
sys.path.append("..")
import pandas as pd
import requests
import json


PROMPT_TEMPLATE={
  "model": "string",
  "messages": [
    {
      "role": "user",
      "content": ""
    }
  ],
  "temperature": 0.01,
  "top_p": 0.7,
  "n": 1,
  "max_tokens": 4096,
  "stream": "false"
}


def get_usecases(test_file):
    use_cases = []
    try:
        df = pd.read_excel(test_file).replace("\r\n", "")
        print(df['Prompt模板提问'])
        use_cases = df['Prompt模板提问'].tolist()
    except Exception as e:
        print("client_utils.get_usecases:=====", str(e))
    finally:
        return use_cases


def generate(url, question):
    text = ""
    try:
        headers = {"accept": "application/json", "Content-Type": "application/json"}

        PROMPT_TEMPLATE["messages"][0]["content"] = question
        print("generate data ====", PROMPT_TEMPLATE)

        ## post的时候，将data字典形式的参数用json包转换成json格式。
        response = requests.post(url=url, headers=headers, data=json.dumps(PROMPT_TEMPLATE))

        ## 获取返回的响应信息
        text = response.json()

        response.close()
    except Exception as e:
        text = str(e)
    finally:
        print("generate text ==== ", text)
        return text


def get_answer(url, use_cases_list, idx):
    output = ()
    try:
        row_idx = str(idx + 1).zfill(3)
        question = use_cases_list[idx]
        text = generate(url=url, question=question.replace("\n", ""))
        answer = text['choices'][0]["message"]["content"]
        print('{} 问题: {} 回答：{} '.format(row_idx, question, answer))
        output = (row_idx, question, answer)
    except Exception as e:
        print("utils.get_answer: ", str(e))
        output = ()
    finally:
        return output


def get_answers(url, use_cases_list):
    outputs = []
    try:
        num_usecases = len(use_cases_list)
        for idx in range(num_usecases):
            output = get_answer(url, use_cases_list, idx)
            outputs.append(output)
    except Exception as e:
        print("utils.get_answers: ", str(e))
        outputs = []
    finally:
        return outputs


import xlwt
def save_to_excel(outputs, output_file_name):
    try:
        rows = len(outputs)
        print("save_to_excel: ", outputs)
        if rows > 0:
            # 创建一个 workbook 对象，这就相当于创建了一个 Excel 文件
            workbook = xlwt.Workbook()

            # 创建一个 sheet 对象，一个 sheet 对象对应一个工作表
            sheet = workbook.add_sheet("Sheet1")

            # 写入表格抬头
            sheet.write(0, 0, "序号")
            sheet.write(0, 1, "问题")
            sheet.write(0, 2, "回复")

            # 循环将元组数据写入表格
            for i, tup in enumerate(outputs):
                for j, value in enumerate(tup):
                    sheet.write(i + 1, j, value)

            # 保存 Excel 文件
            workbook.save(output_file_name)
    except Exception as e:
        print("", str(e))


if __name__ == '__main__':

    # 读出用例文件中问题进入数组
    test_file = "../datas/usecases/reading_undestanding_compact_jinja.xlsx"

    use_cases_list = get_usecases(test_file)
    print("用例数量：", len(use_cases_list))

    # 定义手工启动好的可访问 LLM 服务
    api_llm_url = "http://172.16.0.122:8000/v1/chat/completions"

    # 测试一个答案
    # idx = 0
    #
    # text = get_answer(api_llm_url, use_cases_list, idx)
    # print("answer: ", text)

    # 循环测试全部用例，并保存结果在输出目录当中
    output_file = "./output/Qwen-72B-Chat-20231204.xlsx"
    test_results = get_answers(api_llm_url, use_cases_list)
    save_to_excel(test_results, output_file)



