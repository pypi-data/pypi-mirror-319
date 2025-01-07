from collections import deque


class PopIO:
    def __init__(self):
        self.deque = deque()
        self.closed = False
        self.ignore = False

    def write(self, data):
        if not self.ignore:
            self.deque.append(data)

    def pop(self):
        while self.deque:
            yield self.deque.popleft()

    def tell(self):
        pass

    def seekable(self):
        return True

    def seek(self, position, pivot):
        self.ignore = True
