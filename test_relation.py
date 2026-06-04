from app.services.relation import build_relation_index

messages = [
    {
        "time": "2025-06-01 10:00",
        "score": 1
    },
    {
        "time": "2025-06-01 11:00",
        "score": 2
    },
    {
        "time": "2025-06-01 12:00",
        "score": -1
    }
]

result = build_relation_index(messages)

print(result)