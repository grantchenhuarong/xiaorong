import openai
from common import get_api_key

def gpt_35_api_stream(api_key: str, messages: list):
    """为提供的对话消息创建新的回答 (流式传输)

    Args:
        messages (list): 完整的对话消息
        api_key (str): OpenAI API 密钥

    Returns:
        tuple: (results, error_desc)
    """
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            stream=True,
        )
        completion = {'role': '', 'content': ''}
        for event in response:
            if event['choices'][0]['finish_reason'] == 'stop':
                print(f'收到的完成数据: {completion}')
                break
            for delta_k, delta_v in event['choices'][0]['delta'].items():
                print(f'流响应数据: {delta_k} = {delta_v}')
                completion[delta_k] += delta_v
        messages.append(completion)  # 直接在传入参数 messages 中追加消息
        return (True, '')
    except Exception as err:
        return (False, f'OpenAI API 异常: {err}')

if __name__ == '__main__':
    messages = [{'role': 'system', 'content': '你是一个乐于助人的诗人。'},
                {'role': 'user', 'content': '作一首诗，要有风、要有肉，要有火锅、要有雾，要有美女、要有驴！'},]
    api_key = get_api_key()
    print(gpt_35_api_stream(api_key, messages))
    print(messages)