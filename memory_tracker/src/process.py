class Process:
    def __init__(self, pid, size):
        self.pid = pid
        self.size = size
        self.status = "Running"

    def terminate(self):
        self.status = "Terminated"

    def __repr__(self):
        return f"Process({self.pid}, Size={self.size}, Status={self.status})"
