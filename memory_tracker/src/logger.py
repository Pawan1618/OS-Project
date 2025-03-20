import datetime

def log_memory_action(action, process):
    with open("../logs/memory_log.txt", "a") as file:
        file.write(f"{datetime.datetime.now()} - {action}: {process}\n")
