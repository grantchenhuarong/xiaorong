PROMPT_TEMPLATE = """已知信息：
{context} 
从上述已知信息，选择内容来回答用户的问题，不能添加已知信息之外的内容。如果无法从中得到答案，请直接回答 “根据已知信息无法回答该问题” 或 “没有提供足够的相关信息”。 
问题是：{question}"""

USER_QUESTION_TEMPLATE = """
Human:问题是：{question}"""

ASSISTANT_ANSWER_TEMPLATE = """
Assistant:{answer}"""

NO_ANSWER = "根据已知信息无法回答该问题"