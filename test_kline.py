from app.services.relation import build_relation_index
from app.services.kline_generator import generate_kline

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
    },
    {
        "time": "2025-06-01 13:00",
        "score": 4
    }
]

index_data = build_relation_index(messages)

print("关系指数：")
print(index_data)

kline_data = generate_kline(index_data)

print("K线数据：")
print(kline_data)