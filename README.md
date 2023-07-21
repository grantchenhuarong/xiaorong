# xiaorong
Train one acceptable robot to read and understand Chinese materials.

#0 Do some data collections
## c3
## cail
## cmrc
## drcd
## dureader
## medicine
## military
## pCLUE
## squad
## webqa
## yiqing

#1 Uniform the data format 
According to the multiturn dialogs training's requirements in the project LLaMA-Efficient-Tuning, we modify the data format as following. 
```
{
"instruction": "Human:你好，你能帮我解答一个问题吗？\nAssistant: 当然，请问有什么问题？\nHuman:我想了解人工智能的未来发展方向，你有什么想法吗？\nAssistant: 人工智能在未来的发展方向可能包括更强大的机器学习算法，更先进的自然语言处理技
术，以及更加智能的机器人。此外，人工智能还可以帮助解决许多现实世界的问题，例如自动化和改善医疗保健等领域。\nHuman:听起来很不错。人工智能可能在哪些方面面临挑战呢？\nAssistant:", 
"input": "", 
"output": " 人工智能面临的挑战包括数据隐私、安全和道德方面的问题，以及影响就业机会的自动化等问题。此外，人工智能可能会带来不平等和歧视风险，这也是需要关注的问题。"
}
```
We add the prefix like:
基于上下文的prompt模版，请务必保留"{question}"和"{context}"
```
PROMPT_TEMPLATE = """已知信息：
{context} 

从上述已知信息，选择内容来回答用户的问题，不能添加已知信息之外的内容。如果无法从中得到答案，请说 “根据已知信息无法回答该问题” 或 “没有提供足够的相关信息”。 \r\n问题是：{question}"""
```

## c3
```
 [
  [
   "男：听说你们公司要派你去南方工作?",
   "女：是呀，虽说那边环境好，待遇也不错，可我还是觉得在家里最好。"
  ],
  [
   {
    "question": "他们在谈论什么?",
    "choice": [
     "旅行",
     "坏境",
     "工作",
     "家庭"
    ],
    "answer": "工作"
   }
  ],
  "47-275"
 ]
```
===========================>>>>
```
{
"instruction": "Human:已知信息：\n男：听说你们公司要派你去南方工作?\n女：是呀，虽说那边环境好，待遇也不错，可我还是觉得在家里最好。可选答案有旅行，坏境，工作，家庭。\n
从上述已知信息，选择内容来回答用户的问题，不能添加已知信息之外的内容。如果无法从中得到答案，请说 “根据已知信息无法回答该问题” 或 “没有提供足够的相关信息”。\r\n问题是：他们在谈论什么?\nAssistant:", 
"input": "", 
"output": "工作"
}
```
## cail
## cmrc
## drcd
## dureader
## medicine
## military
## pCLUE
## squad
## webqa
## yiqing


#2 base llm models selection
## llama2?

## chatglm6b

## baichuan7b-sft-8k

#3 Trainning
