from analyzer import generate_memory_usage_graph
import tkinter as tk


def show_report(self):
    generate_memory_usage_graph()


tk.Button(self, text="View Memory Report",
          command=self.show_report).pack(side=tk.BOTTOM, padx=10)
