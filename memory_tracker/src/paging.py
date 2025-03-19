from memory_manager import MemoryManager

class PagingMemoryManager(MemoryManager):
    def __init__(self, total_memory, page_size):
        super().__init__(total_memory)
        self.page_size = page_size
        self.pages = [None] * (total_memory // page_size)

    def allocate_memory(self, process):
        pages_needed = -(-process.size // self.page_size)
        allocated_pages = []

        for i in range(len(self.pages)):
            if len(allocated_pages) == pages_needed:
                break
            if self.pages[i] is None:
                self.pages[i] = process.pid
                allocated_pages.append(i)

        if len(allocated_pages) < pages_needed:
            return False  # Not enough memory
        
        self.used_memory += process.size
        return allocated_pages

    def free_memory(self, process):
        for i in range(len(self.pages)):
            if self.pages[i] == process.pid:
                self.pages[i] = None
        self.used_memory -= process.size
