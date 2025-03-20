import logging

logging.basicConfig(filename="logs/memory_log.txt", level=logging.INFO,
                    format="%(asctime)s - %(message)s", filemode="w")


def log_memory_event(event):
    logging.info(event)
