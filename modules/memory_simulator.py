import numpy as np
from enum import Enum

class AllocationStrategy(Enum):
    FIRST_FIT = 1
    BEST_FIT = 2
    WORST_FIT = 3

class MemorySimulator:
    def __init__(self, total_memory=2048, page_size=64):
        self.total_memory = total_memory
        self.page_size = page_size
        self.memory = np.zeros(total_memory, dtype=int)
        self.processes = {}
        self.free_blocks = [(0, total_memory - 1)]
        self.strategy = AllocationStrategy.FIRST_FIT
        self.history = []
        
    def reset(self):
        self.memory.fill(0)
        self.free_blocks = [(0, self.total_memory - 1)]
        self.processes = {}
        self.history.append(("System Reset", None))
        
    def set_strategy(self, strategy):
        self.strategy = strategy
        
    def allocate_segment(self, process_id, size):
        if process_id in self.processes:
            return False, "Process already exists"
            
        if self.strategy == AllocationStrategy.FIRST_FIT:
            block_index = self._find_first_fit(size)
        elif self.strategy == AllocationStrategy.BEST_FIT:
            block_index = self._find_best_fit(size)
        else:  # WORST_FIT
            block_index = self._find_worst_fit(size)
            
        if block_index == -1:
            return False, "No suitable block found"
            
        start, end = self.free_blocks[block_index]
        self.memory[start:start+size] = process_id
        
        # Update free blocks
        del self.free_blocks[block_index]
        if start + size <= end:
            self.free_blocks.insert(block_index, (start + size, end))
            
        self.processes[process_id] = (start, size)
        self.history.append((f"Allocated segment for {process_id}", (process_id, start, size)))
        return True, f"Allocated {size} units at {start}"
        
    def allocate_pages(self, process_id, size):
        if process_id in self.processes:
            return False, "Process already exists"
            
        pages_needed = (size + self.page_size - 1) // self.page_size
        free_pages = []
        
        # Find all free pages
        for i in range(0, self.total_memory, self.page_size):
            if np.all(self.memory[i:i+self.page_size] == 0):
                free_pages.append(i)
                if len(free_pages) == pages_needed:
                    break
                    
        if len(free_pages) < pages_needed:
            return False, "Not enough free pages"
            
        # Allocate pages
        allocated = []
        for page_start in free_pages:
            self.memory[page_start:page_start+self.page_size] = process_id
            allocated.append((page_start, self.page_size))
            
        self.processes[process_id] = allocated
        self._update_free_blocks()
        self.history.append((f"Allocated pages for {process_id}", (process_id, allocated)))
        return True, f"Allocated {pages_needed} pages"
        
    def deallocate(self, process_id):
        if process_id not in self.processes:
            return False, "Process not found"
            
        allocation = self.processes[process_id]
        
        if isinstance(allocation, tuple):  # Segment
            start, size = allocation
            self.memory[start:start+size] = 0
        else:  # Pages
            for page_start, page_size in allocation:
                self.memory[page_start:page_start+page_size] = 0
                
        del self.processes[process_id]
        self._update_free_blocks()
        self.history.append((f"Deallocated {process_id}", process_id))
        return True, f"Deallocated {process_id}"
        
    def _update_free_blocks(self):
        # Rebuild free blocks by finding contiguous zeros
        self.free_blocks = []
        in_block = False
        start = 0
        
        for i in range(self.total_memory):
            if self.memory[i] == 0 and not in_block:
                in_block = True
                start = i
            elif self.memory[i] != 0 and in_block:
                in_block = False
                self.free_blocks.append((start, i-1))
                
        if in_block:
            self.free_blocks.append((start, self.total_memory-1))
            
    def _find_first_fit(self, size):
        for i, (start, end) in enumerate(self.free_blocks):
            block_size = end - start + 1
            if block_size >= size:
                return i
        return -1
        
    def _find_best_fit(self, size):
        best_index = -1
        min_diff = float('inf')
        
        for i, (start, end) in enumerate(self.free_blocks):
            block_size = end - start + 1
            if block_size >= size and (block_size - size) < min_diff:
                min_diff = block_size - size
                best_index = i
                
        return best_index
        
    def _find_worst_fit(self, size):
        worst_index = -1
        max_size = -1
        
        for i, (start, end) in enumerate(self.free_blocks):
            block_size = end - start + 1
            if block_size >= size and block_size > max_size:
                max_size = block_size
                worst_index = i
                
        return worst_index
        
    def get_memory_state(self):
        return self.memory.copy()
        
    def get_fragmentation(self):
        total_free = sum(end - start + 1 for start, end in self.free_blocks)
        if not self.free_blocks:
            return 0, 0
            
        # External fragmentation (percentage of free memory that can't be used for a request)
        max_block = max(end - start + 1 for start, end in self.free_blocks)
        if total_free == 0:
            external = 0
        else:
            external = (1 - max_block / total_free) * 100
            
        # Internal fragmentation (for pages)
        internal = 0
        for process_id, allocation in self.processes.items():
            if isinstance(allocation, list):  # Paged allocation
                for page_start, page_size in allocation:
                    used = np.count_nonzero(self.memory[page_start:page_start+page_size] == process_id)
                    internal += page_size - used
                    
        return external, internal
        
    def get_utilization(self):
        used = np.count_nonzero(self.memory)
        return (used / self.total_memory) * 100