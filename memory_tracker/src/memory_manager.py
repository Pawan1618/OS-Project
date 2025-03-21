class MemoryManager:
    def _init_(self, total_memory):
        self.total_memory = total_memory
        self.used_memory = 0

    def allocate_memory(self, process):
        raise NotImplementedError

    def free_memory(self, process):
        raise NotImplementedError
