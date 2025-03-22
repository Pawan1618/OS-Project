import psutil
import time

def get_memory_usage():
    """Returns the current memory usage in MB."""
    return psutil.virtual_memory().used / (1024 * 1024)

def track_memory(interval=1):
    """Tracks memory usage at regular intervals."""
    while True:
        memory_usage = get_memory_usage()
        print(f"Memory Usage: {memory_usage:.2f} MB")
        time.sleep(interval)
