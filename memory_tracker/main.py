# <<<<<<< HEAD
from src.paging import PagingMemoryManager
from src.segmentation import SegmentationMemoryManager
from src.process import Process

if __name__ == "__main__":
    mem_manager = PagingMemoryManager(total_memory=1024, page_size=64)

    p1 = Process(1, 128)
    mem_manager.allocate_memory(p1)
    print("Memory allocated:", mem_manager.pages)
# =======
from src.gui import MemoryVisualizer

if __name__ == "__main__":
    app = MemoryVisualizer()
    app.mainloop()
# >>>>>>> origin/gui
