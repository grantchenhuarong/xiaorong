# pip install openai

import time
from common import get_api_key, get_assistant_id_math
from openai import OpenAI

'''
Create an Assistant in the API by defining its custom instructions and picking a model. If helpful, enable tools like Code Interpreter, Retrieval, and Function calling.
Create a Thread when a user starts a conversation.
Add Messages to the Thread as the user ask questions.
Run the Assistant on the Thread to trigger responses. This automatically calls the relevant tools.
'''
# Step 0: Get key from config file, create client
api_key = get_api_key()
client = OpenAI(
   # defaults to os.environ.get("OPENAI_API_KEY")
   api_key=api_key,
)
print("client", client)

# Step 1: Create an Assistant
# assistant = client.beta.assistants.create(
#     name="Math Tutor",
#     instructions="You are a personal math tutor. Write and run code to answer math questions.",
#     tools=[{"type": "code_interpreter"}],
#     model="gpt-4-1106-preview"
# )
assistant_id = get_assistant_id_math()
assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
print("client", client)

# Step 2: Create a Thread
thread = client.beta.threads.create()

# Step 3: Add a Message to a Thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)
print("client", client)

# Step 4: Run the Assistant
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)

# Step 5: Check the Run status
run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)
print(run.status)

# Step 6: Display the Assistant's Response
while run.status != "completed":
   print(run.status)
   time.sleep(10)  # 等待10秒
   run = client.beta.threads.runs.retrieve(
   thread_id=thread.id,
   run_id=run.id
  )
messages = client.beta.threads.messages.list(
 thread_id=thread.id
)

print(messages.data)