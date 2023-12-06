import time
from openai import OpenAI
from common import get_api_key, get_assistant_id_telepolicy

# Step 0: Get key from config file, create client
api_key = get_api_key()
client = OpenAI(
   # defaults to os.environ.get("OPENAI_API_KEY")
   api_key=api_key,
)

# 1.upload_file
# file_list = []
# file_path = "d:\\work\\2023\\技术管理\\20230215GPT研究\\20231124GPTs应用研究\\文件资料\\20220825 《TCA 009—2020 城市道路智慧综合杆工程技术规范》.pdf"
# file = open(file_path, "rb")
# upload_file = client.files.create(file=file, purpose="assistants")
# status = client.files.retrieve(upload_file.id).status
#
# start_time = time.time()
# while status != "processed":
#     print(f"Uploading file,Status:{status}... {time.time() - start_time:.2f}s", end="\r", flush=True)
#     time.sleep(5)
#     status = client.files.retrieve(upload_file.id).status
# print(f"File {upload_file.id} uploaded after {time.time() - start_time:.2f} seconds.")
#
# file_list.append(upload_file.id)
# print("file_id: ", upload_file.id)

# 2. Create an assistant，tools可选code_interpreter，retrieval，自定义function
assistant_id = get_assistant_id_telepolicy()
assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)

# 3. Create a thread ，这里也可以上传文件
# 请根据实际情况修改
#thread_user_prompt = '''你是一位通信技术规范资深专家，请通读已经上传好的文件，根据文章内容智能回答用户提问，并列出回答对应相关文件的具体出处。'''
thread_user_prompt = ""
thread_message = [{"role": "user", "content": thread_user_prompt}]
thread = client.beta.threads.create(messages=thread_message)

# 4. Create a message
user_content = ["哪些相关设备可挂载在智慧综合杆上？",
                "遇到哪些情况时，宜采用智慧综合杆形式规划建设?",
                "一键呼叫设备能够安装在智慧综合杆上么？",
                "智慧综合杆宜采用双路供电么？",
                "综合杆的杆体安装偏差应如何控制？",
                "智慧综合杆工程验收技术文件应包括哪些内容?"]  # 请根据实际情况修改
'''
3.1 道路照明设备、移动通信基站设备、安全防范设备、道路交通标志、公共交通客运标志、公共标
识、道路交通信号设备、道路交通智能化管理设备、气象监测设备、环境监测设备、信息发布设备、
能源供配设备、智能停车设备、城市管理设备、路侧单元设备、有（无）轨电车供电线网设备、公共
广播设备、地下管廊监测设备、一键呼叫设备等城市道路内相关设备可挂载在智慧综合杆上。

4.2.5 遇到下列情况之一时，宜采用智慧综合杆形式规划建设：
1 交通运输繁忙或路内杆件设施较多的人行道、城市主干道等建设工程地段。
2 城市核心区、商业区、重要广场、主要道路的交叉口等。
3 道路宽度难以满足布设多种设施的路段。
4 重要的公共空间。
5 不宜开挖路面的路段。

是的，一键呼叫设备可以安装在智慧综合杆上。根据《TCA 009—2020 城市道路智慧综合杆工程技术规范》中的6.2.18.1条款，通过在智慧综合杆上安装一键呼叫按钮模块、一键呼叫处理模块和可视对讲模块可以实现应急呼叫及应答。这些设备应使用智慧综合杆预留的安装插口进行灵活安装，并且一键呼叫设备应能够远程集中管理和控制，并且需要符合相关要求【12†source】。

是的，智慧综合杆宜采用双路供电。根据《TCA 009—2020 城市道路智慧综合杆工程技术规范》第10.1.10条款，智慧综合杆应使用一路供电用于路灯照明的分时段供电，另一路用于移动通信、视频监控、气象环境、交通安防等挂载设备的全天候供电【12†source】。

【表格内容查询】综合杆的杆体安装偏差应当控制在一定范围内以确保结构稳固，其具体要求规定综合杆的主杆与副杆、主杆与悬臂的装配应采用高强度螺栓，双螺帽紧固【14†source】。标准文件中并没有详细说明具体的偏差数值限制，可能需要配合其他相关细则或安装标准来确定具体的偏差控制要求。如果需要更精确的偏差控制数值或方法，请提供或查询相关的补充标准。

'''

content=user_content[1]
print("content:~~~", content)
thread_message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=content,
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