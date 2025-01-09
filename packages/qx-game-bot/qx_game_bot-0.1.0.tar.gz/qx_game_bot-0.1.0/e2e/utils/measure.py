import time


class Measure:
    def __enter__(self):
        self.startTime = time.time()

    def __exit__(self, *args):
        endTime = time.time()
        executionTime = endTime - self.startTime
        print(f"Execution time: {executionTime*1000:.2f}ms")
