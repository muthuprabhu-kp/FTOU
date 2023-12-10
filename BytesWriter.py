from collections import deque
from threading import Thread


class Writer(object):
    def __init__(self, file_name):
        self.file = open(file_name, "wb")
        self.running = False
        self.queue = deque()
        self.thread = Thread(target=self._writer_thread)

    def close(self):
        """
        Wait for the writer thread to finish and close the open file.
        """
        self.running = False
        self.thread.join()
        self.file.close()

    def add_chunk(self, chunk):
        """
        Adds chunk to the writer queue.
        Starts the writer thread if it's down.
        """
        self.queue.append(chunk)

    def _writer_thread(self):
        """
        Runs until a stop is requested and the queue is exhausted.
        """
        self.running = True
        while self.running or len(self.queue):
            if len(self.queue):
                chunk, data = self.queue.popleft()
                self.file.seek(chunk*self.chunk_size)
                self.file.write(data)

