from typing import Final
import re
import time
import inspect
from functools import wraps

PROFILE:bool = True
HEADER_PRINTER:bool = False

def profile_decorator(func: callable) -> callable:
    # Initialize a counter for function calls
    func._call_count = 0

    @wraps(func)
    def wrapper(*args, **kwargs) -> callable:
        global HEADER_PRINTER
        
        if not PROFILE:
            return func(*args, **kwargs)

        # Increment the function call counter
        func._call_count += 1

        # Get the frame information of the caller
        frame: Final[object] = inspect.currentframe().f_back
        filename: Final[str] = frame.f_code.co_filename
        filename = re.search(r"(\w+.py)", filename)
        filename = filename.group()
        lineno: Final[int] = frame.f_lineno

        # Start measuring CPU and wall time
        start_cpu: Final[float] = time.process_time_ns()
        start_wall: Final[float] = time.perf_counter_ns()

        # Execute the function
        result = func(*args, **kwargs)

        # Stop measuring CPU and wall time
        end_cpu: Final[float] = time.process_time_ns()
        end_wall: Final[float] = time.perf_counter_ns()

        # Calculate the elapsed times
        cpu_time: Final[float] = (end_cpu - start_cpu) / 1e9  # Convert nanoseconds to seconds
        wall_time: Final[float] = (end_wall - start_wall) / 1e9  # Convert nanoseconds to seconds

        # Log the details in table format
        if not HEADER_PRINTER:
            print(f"{'Function name':<15} {'filename':<15} {'line':<5} {'count':<5} {'cpu':<10} {'wall':<10}")
            HEADER_PRINTER = True

        print(f"{func.__name__:<15} {filename:<15} {lineno:<5} {func._call_count:<5} {cpu_time:<10.6f} {wall_time:<10.5f}")

        return result

    return wrapper

@profile_decorator
def func1():
    total:int = 0
    for _ in range(1000000):
        total += sum(i * i for i in range(100))

@profile_decorator
def func2():
    total:int = 0
    for _ in range(1000000):
        total += sum(i * i for i in range(100))

if __name__ == "__main__":
    # call to func1
    func1()
    func1()
    func1()

    # call to func2
    func2()
    func2()