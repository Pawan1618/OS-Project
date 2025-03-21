class Process:
    def __init__(self, process_id, name, memory_size):
        self.process_id = process_id
        self.name = name
        self.memory_size = memory_size
        self.state = "NEW"  # States: NEW, RUNNING, WAITING, TERMINATED
        self.allocation_time = None
        self.segments = []  # List of memory segments allocated to this process

    def update_state(self, new_state):
        """Update process state"""
        self.state = new_state

    def add_segment(self, segment):
        """Add a memory segment to the process"""
        self.segments.append(segment)

    def clear_segments(self):
        """Clear all memory segments"""
        self.segments.clear()

    def get_total_memory(self):
        """Get total memory allocated to the process"""
        return sum(segment['size'] for segment in self.segments)

    def __str__(self):
        return f"Process(ID={self.process_id}, Name={self.name}, Size={self.memory_size}, State={self.state})"
