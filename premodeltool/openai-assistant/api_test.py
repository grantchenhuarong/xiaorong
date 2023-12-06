import time
from openai import OpenAI
from common import get_plus_api_key, get_all_assistants_by_account, get_files_by_assistant, get_fileinfo_by_fileid


if __name__ == "__main__":
   # 获取 OpenAI 帐号访问秘钥
   api_key = get_plus_api_key()
   client = OpenAI(
      api_key=api_key,
   )

   # 获取该帐号下所有的 Assistant
   ok, assistants = get_all_assistants_by_account(api_key)
   if ok:
      print(assistants['data'])

      for assistant in assistants['data']:
         time.sleep(2)
         assistant_id = assistant['id']
         assistant_name = assistant['name']
         assistant_instructions = bytes(assistant['instructions'], "utf-8").decode('unicode_escape')
         assistant_file_ids = assistant['file_ids']

         for file_id in assistant_file_ids:
            ok, file_info = get_fileinfo_by_fileid(api_key, assistant_id, file_id)
            if ok:
               print(assistant_name, assistant_instructions, file_info)

   # 尝试开设assistant
   instructions = '''
   Role and Goal: The GPT, ‘通信智能小秘’, is an expert in 5G V2X, communication pipeline lightning protection, and smart pole engineering. It uses Mandarin for responding, relying on specific uploaded documents.

Constraints: The GPT uses only the information from these documents, citing sources. It says "无法根据提供知识文档进行回答" if unable to answer from the documents.

Guidelines: The GPT maintains professionalism, using technical language when necessary. It provides detailed, accurate information within the scope of the documents.

Clarification: The GPT asks for clarification on unclear or incomplete questions to ensure relevant and precise responses.

Personalization: The GPT embodies a friendly and patient demeanor, demonstrating technical expertise with a detailed and enthusiastic approach to guidance.
   '''
   assistant = client.beta.assistants.create(
      name="TelePolicyAssitant",
      instructions=instructions,
      tools=[{"type": "code_interpreter"}],
      model="gpt-4-1106-preview"
   )