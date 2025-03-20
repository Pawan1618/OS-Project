import os
from src.logger import log_memory_event, log_csv


def test_log_memory_event():
    log_memory_event("Test Event")
    with open("logs/memory_log.txt", "r") as file:
        assert "Test Event" in file.read()


def test_log_csv():
    log_csv(1, "Allocate")
    assert os.path.exists("reports/memory_usage_report.csv")
