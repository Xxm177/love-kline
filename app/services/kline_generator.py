from collections import defaultdict


def generate_kline(index_data):
    daily = defaultdict(list)

    for item in index_data:
        date = item["time"][:10]
        daily[date].append(item["index"])

    result = []

    for date, values in daily.items():
        result.append(
            {
                "date": date,
                "open": values[0],
                "high": max(values),
                "low": min(values),
                "close": values[-1]
            }
        )

    return sorted(result, key=lambda x: x["date"])