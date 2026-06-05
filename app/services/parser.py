import re

# 格式1: 单行格式  2025-06-01 08:00 小明：早安宝贝
PATTERN_SINGLE = re.compile(
    r"(\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}(?::\d{2})?)\s+(\S+?)[：:](.*)"
)

# 格式2: 微信导出多行格式
#  小明  2025-06-01 08:00
#  早安宝贝
#  或
#  2025-06-01 08:00:00 小明
#  早安宝贝
PATTERN_WECHAT_HEADER_SENDER_FIRST = re.compile(
    r"^(\S+)\s+(\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}(?::\d{2})?)\s*$"
)
PATTERN_WECHAT_HEADER_TIME_FIRST = re.compile(
    r"^(\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}(?::\d{2})?)\s+(\S+)\s*$"
)


def _try_parse_single_line(lines: list[str]) -> list[dict] | None:
    """解析单行格式"""
    messages = []
    for line in lines:
        m = PATTERN_SINGLE.match(line.strip())
        if not m:
            return None
        messages.append({
            "time": m.group(1),
            "sender": m.group(2),
            "message": m.group(3).strip(),
        })
    return messages if messages else None


def _try_parse_wechat(lines: list[str]) -> list[dict] | None:
    """解析微信多行格式（消息分两行）"""
    messages = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # 尝试匹配头部行
        m = PATTERN_WECHAT_HEADER_SENDER_FIRST.match(line)
        if m:
            sender = m.group(1)
            time_str = m.group(2)
        else:
            m = PATTERN_WECHAT_HEADER_TIME_FIRST.match(line)
            if m:
                time_str = m.group(1)
                sender = m.group(2)
            else:
                # 不是头部行，跳过
                i += 1
                continue

        # 收集消息内容（可能多行）
        msg_parts = []
        i += 1
        while i < len(lines):
            next_line = lines[i]
            if not next_line.strip():
                # 空行表示消息结束
                i += 1
                break
            # 检查是否是新消息的头部
            if PATTERN_WECHAT_HEADER_SENDER_FIRST.match(next_line.strip()) or \
               PATTERN_WECHAT_HEADER_TIME_FIRST.match(next_line.strip()):
                break
            msg_parts.append(next_line.strip())
            i += 1

        msg_text = " ".join(msg_parts).strip()
        if msg_text:
            messages.append({
                "time": time_str,
                "sender": sender,
                "message": msg_text,
            })

    return messages if messages else None


def parse_chat(text: str) -> list[dict]:
    lines = text.splitlines()

    # 先试单行格式
    result = _try_parse_single_line(lines)
    if result:
        return result

    # 再试微信多行格式
    result = _try_parse_wechat(lines)
    if result:
        return result

    # 都不匹配，返回空
    return []
