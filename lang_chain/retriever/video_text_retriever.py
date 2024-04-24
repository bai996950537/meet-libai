# -*- coding: utf-8 -*-
# @Time    : 2024/2/24 21:43
# @Author  : nongbin
# @FileName: audio_text_retriever.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from typing import List, Dict

from lang_chain.client import get_ai_client

_PROMPT_ = "请从上述对话中帮我提取出文生视频所对应的文本内容"
__client = get_ai_client()


def __construct_messages(question: str, history: List[List | None]) -> List[Dict[str, str]]:
    messages = [
        {"role": "system", "content": "你现在扮演信息抽取的角色，要求根据用户输入和AI的回答，正确提取出信息，无需包含提示文字"}]

    for user_input, ai_response in history:
        messages.append({"role": "user", "content": user_input})
        messages.append(
            {"role": "assistant", "content": repr(ai_response)})

    messages.append({"role": "user", "content": question})
    messages.append({"role": "user", "content": _PROMPT_})

    return messages


def extract_text(question: str,
                 history: List[List | None] | None = None) -> str:
    response = __client.chat.completions.create(
        model="glm-4",
        messages=__construct_messages(question, history if history else []),
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
    )

    return response.choices[0].message.content
