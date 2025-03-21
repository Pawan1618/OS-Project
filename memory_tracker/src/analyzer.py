import pandas as pd
import matplotlib.pyplot as plt


def generate_memory_usage_graph():
    df = pd.read_csv("reports/memory_usage_report.csv",
                     names=["Process ID", "Action", "Timestamp"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df["Count"] = df["Action"].apply(lambda x: 1 if x == "Allocate" else -1)
    df["Total Allocations"] = df["Count"].cumsum()

    plt.figure(figsize=(10, 5))
    plt.plot(df["Timestamp"], df["Total Allocations"],
             marker='o', linestyle='-')
    plt.xlabel("Time")
    plt.ylabel("Memory Usage")
    plt.title("Memory Allocation Over Time")
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()
