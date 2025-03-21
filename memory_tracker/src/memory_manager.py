class MemoryManager:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.used_memory = 0
        self.memory_blocks = []  # List of memory segments
        self.processes = {}      # Dictionary to track processes and their memory segments

    def allocate_memory(self, process_id, size):
        """
        Allocates memory for a process using best-fit algorithm
        Returns allocated segment or None if allocation fails
        """
        if size > self.total_memory - self.used_memory:
            return None  # Not enough memory

        # Find the best fitting free block
        best_block = None
        best_block_size = float('inf')
        best_block_index = -1

        for i, block in enumerate(self.memory_blocks):
            if not block['used'] and block['size'] >= size:
                if block['size'] < best_block_size:
                    best_block = block
                    best_block_size = block['size']
                    best_block_index = i

        if best_block is None:
            # No suitable block found, create new if possible
            if not self.memory_blocks:
                new_block = {
                    'start': 0,
                    'size': size,
                    'process_id': process_id,
                    'used': True
                }
                self.memory_blocks.append(new_block)
                self.processes[process_id] = [new_block]
                self.used_memory += size
                return new_block
            return None

        # Split the block if it's too large
        if best_block['size'] > size:
            new_block = {
                'start': best_block['start'] + size,
                'size': best_block['size'] - size,
                'process_id': None,
                'used': False
            }
            best_block['size'] = size
            self.memory_blocks.insert(best_block_index + 1, new_block)

        best_block['used'] = True
        best_block['process_id'] = process_id
        
        if process_id not in self.processes:
            self.processes[process_id] = []
        self.processes[process_id].append(best_block)
        self.used_memory += size
        return best_block

    def free_memory(self, process_id):
        """
        Frees all memory segments allocated to a process
        Returns the amount of memory freed
        """
        if process_id not in self.processes:
            return 0

        freed_memory = 0
        for block in self.processes[process_id]:
            block['used'] = False
            block['process_id'] = None
            freed_memory += block['size']

        self.used_memory -= freed_memory
        del self.processes[process_id]
        
        # Merge adjacent free blocks
        self._merge_free_blocks()
        return freed_memory

    def _merge_free_blocks(self):
        """Merges adjacent free memory blocks to reduce fragmentation"""
        i = 0
        while i < len(self.memory_blocks) - 1:
            current_block = self.memory_blocks[i]
            next_block = self.memory_blocks[i + 1]
            
            if not current_block['used'] and not next_block['used']:
                current_block['size'] += next_block['size']
                self.memory_blocks.pop(i + 1)
            else:
                i += 1

    def get_fragmentation_info(self):
        """
        Returns information about memory fragmentation
        """
        free_blocks = [block for block in self.memory_blocks if not block['used']]
        total_free = sum(block['size'] for block in free_blocks)
        largest_free = max((block['size'] for block in free_blocks), default=0)
        
        return {
            'total_memory': self.total_memory,
            'used_memory': self.used_memory,
            'free_memory': total_free,
            'largest_free_block': largest_free,
            'fragmentation_percentage': ((total_free - largest_free) / self.total_memory * 100) if total_free > 0 else 0
        }

    def get_memory_map(self):
        """
        Returns the current memory map for visualization
        """
        return self.memory_blocks
