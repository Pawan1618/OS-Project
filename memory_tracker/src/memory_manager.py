from logger import log_memory_event


def allocate_memory(self, process):
    success = self._allocate(process)
    if success:
        log_memory_event(
            f"Allocated Process {process.pid} with size {process.size}")
    return success


def free_memory(self, process_id):
    self._free(process_id)
    log_memory_event(f"Freed memory of Process {process_id}")
