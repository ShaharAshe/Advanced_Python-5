from typing import Final
import re
import time
import inspect
from functools import wraps
from contextlib import ContextDecorator

# global variables
PROFILE:bool = True
HEADER_PRINTER:bool = False

class ProfileBlock(ContextDecorator):
    def __init__(self, func_name="ProfileBlock"):
        self.func_name = func_name

    def __enter__(self):
        global HEADER_PRINTER

        if not PROFILE:
            return self

        # Get the frame information of the caller
        self.frame = inspect.currentframe().f_back
        self.filename = self.frame.f_code.co_filename
        self.filename = re.search(r"(\w+.py)", self.filename)
        self.filename = self.filename.group()
        self.lineno = self.frame.f_lineno

        # Start measuring CPU and wall time
        self.start_cpu = time.process_time()
        self.start_wall = time.perf_counter()

        # Initialize call count
        if not hasattr(self, 'call_count'):
            self.call_count = 0

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not PROFILE:
            return

        # Stop measuring CPU and wall time
        end_cpu = time.process_time()
        end_wall = time.perf_counter()

        # Calculate the elapsed times
        cpu_time = end_cpu - self.start_cpu
        wall_time = end_wall - self.start_wall

        # Increment the call count
        self.call_count += 1

        # Print the header if not already printed
        global HEADER_PRINTER
        if not HEADER_PRINTER:
            print(f"{'Function name':<15} {'filename':<15} {'line':<5} {'count':<5} {'cpu':<10} {'wall':<10}")
            HEADER_PRINTER = True

        # Log the details in table format
        print(f"{self.func_name:<15} {self.filename:<15} {self.lineno:<5} {self.call_count:<5} {cpu_time:<10.6f} {wall_time:<10.5f}")

def func1():
    with ProfileBlock("func1"):
        total = 0
        for _ in range(1000000):
            total += sum(i * i for i in range(100))
def func2():
    with ProfileBlock("func2"):
        total = 0
        for _ in range(1000000):
            total += sum(i * i for i in range(100))

if __name__ == "__main__":
    with ProfileBlock("main block"):
        # call to func1
        func1()
        func1()
        func1()

        # call to func2
        func2()
        func2()
