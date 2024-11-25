import sys

def parse_log_line(line: str) -> dict:
    parts = line.split(maxsplit=3)
    if len(parts) < 4:
        return {}
    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "message": parts[3]
    }

def load_logs(file_path: str) -> list:
    try:
        with open(file_path, 'r') as file:
            return [parse_log_line(line) for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка під час читання файлу: {e}")
        sys.exit(1)

def filter_logs_by_level(logs: list, level: str) -> list:
    return [log for log in logs if log.get("level", "").upper() == level.upper()]

def count_logs_by_level(logs: list) -> dict:
    counts = {}
    for log in logs:
        level = log.get("level", "")
        counts[level] = counts.get(level, 0) + 1
    return counts

def display_log_counts(counts: dict):
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level, count in counts.items():
        print(f"{level:<16} | {count}")

if __name__ == "__main__":
    log_file = sys.argv[1]
    log_level = sys.argv[2] if len(sys.argv) > 2 else None

    logs = load_logs(log_file)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if log_level:
        filtered_logs = filter_logs_by_level(logs, log_level)
        print(f"\nДеталі логів для рівня '{log_level.upper()}':")
        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")