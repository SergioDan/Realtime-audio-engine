import time
from collections import deque

class JitterBuffer:
    def __init__(self, max_size=50):
        self.buffer = deque()
        self.max_size = max_size

    def push(self, packet):
        """Add a packet (sequence_number, timestamp, payload)."""
        self.buffer.append(packet)
        self.buffer = deque(sorted(self.buffer, key=lambda x: x[0]))

        if len(self.buffer) > self.max_size:
            self.buffer.popleft()

    def pop(self):
        """Return next packet in order."""
        if self.buffer:
            return self.buffer.popleft()
        return None
