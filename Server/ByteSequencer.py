from collections import deque
from threading import Thread


class Sequencer:
    def __init__(self, name):
        self.name = name
        self.file = open(name, "wb")
        self.queue = deque()
        self.running = False
        self.byte_sequence = []
        self.thread = Thread(target=self._writer_thread)

    def add(self, byte):
        index = byte['index']
        self.queue.append(byte)
        # self.byte_sequence.append(byte)
        # self.arrange()
        pass

    def close(self):
        """
        Wait for the writer thread to finish and close the open file.
        """
        self.running = False
        self.thread.join()
        self.file.close()

    def _writer_thread(self):
        """
        Runs until a stop is requested and the queue is exhausted.
        """
        self.running = True
        while self.running or len(self.queue):
            if len(self.queue):
                byte = self.queue.popleft()
                chunk = byte['index']
                data = byte['data']
                chunk_size = len(data)
                self.file.seek(chunk*chunk_size)
                self.file.write(data)

    def arrange(self):
        self.byte_sequence.sort(key=lambda x: x['index'])
        i = 0
        while i != len(self.byte_sequence):
            current = self.byte_sequence[i]
            previous = self.byte_sequence[i - 1]
            current_sequence = current.get('index')
            previous_sequence = previous.get('last', previous.get('index'))
            if (current_sequence - 1) == previous_sequence and (current_sequence - 1) > -1:
                current = self.byte_sequence.pop(i)
                previous['data'] = previous['data'] + current.get('data', b'')
                last_sequence = current.get('last', current.get('index'))
                previous['last'] = last_sequence
                continue
            i += 1
        print(self.byte_sequence)


if __name__ == '__main__':
    obj = Sequencer('test')
    obj.add({'index': 0, 'data': b'0'})
    obj.add({'index': 1, 'data': b'1'})
    obj.add({'index': 2, 'data': b'2'})
    obj.add({'index': 3, 'data': b'3'})
    obj.add({'index': 4, 'data': b'4'})
    obj.add({'index': 5, 'data': b'5'})
    obj.add({'index': 6, 'data': b'6'})
    obj.add({'index': 7, 'data': b'7'})
    obj.add({'index': 8, 'data': b'8'})
    obj.add({'index': 9, 'data': b'9'})
    obj.add({'index': 10, 'data': b'10'})
    obj.add({'index': 11, 'data': b'11'})
