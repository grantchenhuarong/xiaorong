import time
from openai import OpenAI
from common import get_api_key, get_assistant_id_telepolicy

# Step 0: Get key from config file, create client
api_key = get_api_key()
client = OpenAI(
   # defaults to os.environ.get("OPENAI_API_KEY")
   api_key=api_key,
)

# 2. Create an assistant，tools可选code_interpreter，retrieval，自定义function
assistant_id = get_assistant_id_telepolicy()
assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)

# 3. Create a thread ，这里也可以上传文件
# 请根据实际情况修改
thread_user_prompt = '''
Role and Goal: The GPT, ‘通信智能小秘’, is an expert in 5G V2X, communication pipeline lightning protection, and smart pole engineering. It uses Mandarin for responding, relying on specific uploaded documents.

Constraints: The GPT uses only the information from these documents, citing sources. It says "无法根据提供知识文档进行回答" if unable to answer from the documents.

Guidelines: The GPT maintains professionalism, using technical language when necessary. It provides detailed, accurate information within the scope of the documents.

Clarification: The GPT asks for clarification on unclear or incomplete questions to ensure relevant and precise responses.

Personalization: The GPT embodies a friendly and patient demeanor, demonstrating technical expertise with a detailed and enthusiastic approach to guidance.
'''
thread_message = [{"role": "user", "content": thread_user_prompt}]
thread = client.beta.threads.create(messages=thread_message)

def get_assistant_answer(thread, user_content):
    # print("content:~~~", user_content)
    thread_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_content,
    )

    # 5. Create a run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    run_steps_list = client.beta.threads.runs.steps.list(
        thread_id=thread.id,
        run_id=run.id,
    )

    start_time = time.time()
    while run_steps_list.data == []:
        print(f"thread is starting,{run.status} {time.time() - start_time:.2f}s", end="\r", flush=True)
        # time.sleep(5)
        run_steps_list = client.beta.threads.runs.steps.list(
            thread_id=thread.id,
            run_id=run.id,
        )

    # 6. message creation
    message_id_list = []
    while message_id_list == []:
        for i in run_steps_list.data:
            if i.type == "message_creation" and i.status == "completed":
                message_id_list.append(i.step_details.message_creation.message_id)
        else:
            time.sleep(5)
            print(f"progressing:waiting for 5 seconds...")
            run_steps_list = client.beta.threads.runs.steps.list(
                thread_id=thread.id,
                run_id=run.id,
            )

    # 7. print message
    for i in message_id_list:
        message = client.beta.threads.messages.retrieve(
            message_id=i,
            thread_id=thread.id,
        )
        print(message.content[0].text.value)

# 4. Create a message
user_content = ""
while True:
    user_content = input("\n请输入问题：")

    if user_content.lower() == "bye" :
        print("结束对话，下次再见。")
        break

    get_assistant_answer(thread, user_content)