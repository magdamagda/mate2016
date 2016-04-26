from collections import deque
from PyQt4.Qt import QMutex

class queue:

    def __init__(self, maxSize=10):
        self.maxSize = maxSize
        self._q = deque()
        self.mutex = QMutex()

    def urgentFrame(self, item):
        self.mutex.lock()
        self._q.clear()
        self._q.appendleft(item)
        self.mutex.unlock()

    def push(self, item):
        self.mutex.lock()
        self._q.appendleft(item)
        self.mutex.unlock()

    def pop(self):
        self.mutex.lock()
        item = self._q.pop()
        self.mutex.unlock()
        return item

    def size(self):
        return len(self._q)

    def isEmpty(self):
        return len(self._q)==0
