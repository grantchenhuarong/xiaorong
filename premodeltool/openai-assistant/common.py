import json
import requests
from openai import OpenAI


def get_api_key():
    api_key = ""
    with open("./config/openai-api-key.json", "r") as f:
        config_file = json.load(f)
        api_key = config_file["OpenAI-assistant-secret-key"]
    return api_key


def get_plus_api_key():
    api_key = ""
    with open("./config/openai-api-key.json", "r") as f:
        config_file = json.load(f)
        api_key = config_file["Plus-OpenAI-assistant-secret-key"]
    return api_key


def get_assistant_id_math():
    assitant_id = ""
    with open("./config/openai-api-key.json", "r") as f:
        config_file = json.load(f)
        assitant_id = config_file["math-tutor-assistant-id"]
    return assitant_id


def get_assistant_id_telepolicy():
    assitant_id = ""
    with open("./config/openai-api-key.json", "r") as f:
        config_file = json.load(f)
        assitant_id = config_file["telepolicy-assistant-id"]
    return assitant_id


def get_all_assistants_by_account(api_key):
    endpoint = 'https://api.openai.com/v1/assistants'

    # 发送 GET 请求以获取账户下所有的Assistants信息
    headers = {
        'OpenAI-Beta': 'assistants=v1',
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.get(endpoint, headers=headers)

    assistants = None
    if response.status_code == 200:
        assistants = response.json()
        print("账户下的 Assistants 信息：")
        print(json.dumps(assistants, indent=2))
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")

    return response.status_code, assistants

def get_files_by_assistant(api_key, assistant_id):
    endpoint = f'https://api.openai.com/v1/assistants/{assistant_id}/files'

    # 发送 GET 请求以获取Assistant下所有文件的信息
    headers = {
        'OpenAI-Beta': 'assistants=v1',
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.get(endpoint, headers=headers)

    files_list = None
    if response.status_code == 200:
        files_info = response.json()
        print("Assistant下的文件信息：")
        print(json.dumps(files_info, indent=2))
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")

    return response.status_code, files_list


def get_fileinfo_by_fileid(api_key, assistant_id, file_id):
    # 替换为您的 OpenAI API 密钥和 Assistant ID
    endpoint = f'https://api.openai.com/v1/assistants/{assistant_id}/files/{file_id}'

    headers = {
        'OpenAI-Beta': 'assistants=v1',
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # 发送 GET 请求以获取特定文件的信息
    response = requests.get(endpoint, headers=headers)

    file_info = None
    if response.status_code == 200:
        file_info = response.json()
        print("文件信息：")
        print(json.dumps(file_info, indent=2))
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")

    return response.status_code, file_info