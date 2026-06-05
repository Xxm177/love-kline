import json
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def score_message(message: str) -> dict:
    prompt = f"""
你是关系分析师。

请分析下面这句话对关系的影响。

返回严格JSON：

{{
    "score": 0,
    "dimension": "",
    "reason": ""
}}

评分范围：

-5 非常负面
0 中性
+5 非常积极

消息：

{message}
"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    content = response.choices[0].message.content
    return json.loads(content)


def _score_chunk(messages: list[str]) -> list[dict]:
    indexed = "\n".join(
        f"[{i}] {msg}" for i, msg in enumerate(messages)
    )

    prompt = f"""你是关系分析师。
请分析以下每条消息对关系的影响。

对每条消息返回包含score、dimension、reason的JSON对象。
评分范围：-5(非常负面) 到 +5(非常积极)
dimension可选：关心、亲密、幽默、冲突、冷漠、支持、理解、承诺、分享、赞美

消息列表：

{indexed}

严格返回JSON数组，顺序与消息编号一致，不要遗漏任何一条：

[
  {{"score": 0, "dimension": "", "reason": ""}},
  ...
]"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    content = response.choices[0].message.content

    # Extract JSON array from response (handle markdown code blocks)
    content = content.strip()
    if content.startswith("```"):
        lines = content.split("\n")
        content = "\n".join(lines[1:-1])

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        # Fallback: try to find JSON array in the content
        import re

        match = re.search(r"\[[\s\S]*\]", content)
        if match:
            result = json.loads(match.group())
        else:
            raise

    return result


def score_messages_batch(
    messages: list[str], chunk_size: int = 60
) -> list[dict]:
    all_scores: list[dict] = []
    for i in range(0, len(messages), chunk_size):
        chunk = messages[i : i + chunk_size]
        scores = _score_chunk(chunk)
        all_scores.extend(scores)
    return all_scores
