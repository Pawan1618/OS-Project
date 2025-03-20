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

def draw_memory_grid(self, num_blocks=16):
    block_width = self.winfo_width() // num_blocks
    self.canvas.delete("all")
    
    for i in range(num_blocks):
        x1, y1 = i * block_width, 0
        x2, y2 = (i + 1) * block_width, 50
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")
        
    self.canvas.update()
