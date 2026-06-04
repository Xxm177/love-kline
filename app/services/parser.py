import re
def parse_chat(text:str):
    messages=[]
    pattern=re.compile(
        r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s+(.*?)：(.*)"
    )
    for line in text.splitlines():
        line=line.strip()
        if not line:
            continue

        match=pattern.match(line)

        if match:

            messages.append(
                {
                    "time":match.group(1),
                    "sender":match.group(2),
                    "message":match.group(3)
                }
            )
    return messages