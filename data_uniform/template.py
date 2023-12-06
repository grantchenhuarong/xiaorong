PROMPT_TEMPLATE = """已知信息：
{context} 
从上述已知信息，选择内容来回答用户的问题，不能添加已知信息之外的内容。如果无法从中得到答案，请直接回答 “根据已知信息无法回答该问题” 或 “没有提供足够的相关信息”。 
问题是：{question}"""

PROMPT_TEMPLATE_MIXED = """你是一位知识渊博而且语言逻辑严密的中学语文老师，请认真阅读理解下述已知信息，回答后继问题。要求只能根据已知信息来回答，不添加已知信息之外的内容。要求直接给出答案，如果无法从已知信息中得到答案，请回答 “根据已知信息无法回答该问题”。

已知信息：{context}
 
问题是：{question}"""




USER_QUESTION_TEMPLATE = """
Human:问题是：{question}"""

USER_QUESTION_MOSS_TEMPLATE = """问题是：{question}"""

ASSISTANT_ANSWER_TEMPLATE = """
Assistant:{answer}"""

NO_ANSWER = "根据已知信息无法回答该问题"