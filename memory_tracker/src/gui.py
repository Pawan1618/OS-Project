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

def create_controls(self):
    control_frame = tk.Frame(self)
    control_frame.pack(side=tk.BOTTOM, fill=tk.X)

    tk.Button(control_frame, text="Allocate Process", command=self.allocate_process).pack(side=tk.LEFT, padx=10)
    tk.Button(control_frame, text="Free Process", command=self.free_process).pack(side=tk.LEFT, padx=10)
    
    self.mode_var = tk.StringVar(value="Paging")
    tk.OptionMenu(control_frame, self.mode_var, "Paging", "Segmentation", command=self.toggle_mode).pack(side=tk.RIGHT, padx=10)

from paging import PagingMemoryManager
from segmentation import SegmentationMemoryManager
from process import Process

def allocate_process(self):
    process = Process(pid=len(self.memory_manager.pages) + 1, size=64)
    success = self.memory_manager.allocate_memory(process)
    if success:
        self.draw_memory_grid()

def free_process(self):
    if self.memory_manager.pages:
        process_id = self.memory_manager.pages[-1]
        self.memory_manager.free_memory(process_id)
        self.draw_memory_grid()

def toggle_mode(self, mode):
    self.memory_manager = PagingMemoryManager(1024, 64) if mode == "Paging" else SegmentationMemoryManager(1024)
    self.draw_memory_grid()
