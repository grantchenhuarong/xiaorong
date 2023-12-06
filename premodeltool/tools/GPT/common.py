import time
import requests
import json

def streamGetGPTAnswer(url, HEADERS, payload, question):

    collected_messages = ""

    try:
        payload['messages'][0]['content'] = question
        print(payload)

        response=requests.post(url, headers=HEADERS, data=json.dumps(payload), stream=True)

        # iterate through the stream of events
        end_flag_str = '"finish_reason":"stop"}]}'
        end_flag_str_len = len(end_flag_str)
        chunk_finish_str = '"finish_reason":null}]}'
        chunk_finish_str_len = len(chunk_finish_str)
        chunk_prefix = 'data:'
        chunk_message = "" #用来记录完整chunk消息

        for chunk in response:
            chunk = chunk.decode().replace("\n", "")
            # print("chunk-----", chunk)
            if chunk[-end_flag_str_len:] == end_flag_str: #回复全部结束
                break
            else:
                chunk_len = len(chunk)
                if (chunk_len):
                    finish_pos = chunk.find(chunk_finish_str)
                    if finish_pos != -1: # 完整的Chunk结束，需要提取内容
                        chunk_message += chunk[:finish_pos + chunk_finish_str_len]  # 集合完整chunk
                        chunk_message = chunk_message[len(chunk_prefix):] # 剔除完整chunk的前缀标识data:
                        try:
                            chunk_content = json.loads(chunk_message)["choices"][0]["delta"]["content"]
                        except Exception as e:
                            print("warning: chunk explain error set empty", str(e), chunk_message)
                            chunk_content = ""
                        finally:
                            chunk_message = chunk[finish_pos + chunk_finish_str_len:] # 完成JSON解析后接收chunk的变量清空或者得到剩余部分
                            collected_messages += chunk_content # 完整记录全部信息
                    else:
                        chunk_message += chunk  # 集合chunk

    except Exception as e:
        print(f"Full conversation received: ", collected_messages, str(e))
    finally:
        return collected_messages
