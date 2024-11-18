from datetime import datetime
from functools import wraps
import asyncio

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_time=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.last_failure_time = None
        self.is_open = False

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if self.is_open:
                if (datetime.now() - self.last_failure_time).seconds > self.recovery_time:
                    self.is_open = False
                    self.failure_count = 0
                else:
                    raise Exception("Circuit is open")
            
            try:
                result = await func(*args, **kwargs)
                self.failure_count = 0
                return result
            except Exception as e:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self.is_open = True
                    self.last_failure_time = datetime.now()
                raise e
        return wrapper