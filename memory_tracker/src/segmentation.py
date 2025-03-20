from memory_manager import MemoryManager

class SegmentationMemoryManager(MemoryManager):
    def __init__(self, total_memory):
        super().__init__(total_memory)
        self.segments = []

    def allocate_memory(self, process):
        if self.used_memory + process.size > self.total_memory:
            return False  # Not enough memory

        segment = {'pid': process.pid, 'size': process.size}
        self.segments.append(segment)
        self.used_memory += process.size
        return segment

    def free_memory(self, process):
        self.segments = [s for s in self.segments if s['pid'] != process.pid]
        self.used_memory -= process.size
