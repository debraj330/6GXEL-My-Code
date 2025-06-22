class FifoQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            return {
                'class': None,
                'cqi': None,
                'rssi': None,
                'sinr': None,
                'ni': None
            }

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def __str__(self):
        return '\n'.join(str(value) for value in self.queue)
