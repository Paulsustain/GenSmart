import functools
import time

def retry(retry_count, delay):
    def retry_decorator(func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            result = None
            last_exception = None
            for _ in range(retry_count):
                try:
                    result = func(*args, **kwargs)
                    if result:
                        return result
                except Exception as e:
                    last_exception = e
                time.sleep(delay)
                
            if last_exception is not None:
                print(last_exception)
            
        return func_wrapper
    return retry_decorator
                
            
                