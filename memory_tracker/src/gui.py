import tkinter as tk

class MemoryVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Real-Time Memory Allocation Tracker")
        self.geometry("800x600")

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = MemoryVisualizer()
    app.mainloop()
