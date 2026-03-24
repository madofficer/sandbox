from functools import wraps
from time import perf_counter


def timer(func):
    @wraps(func)
    async def decorator(*args, **kwargs):
        start = perf_counter()
        res = await func(*args, **kwargs)
        end = perf_counter()
        print(f"api call {func.__name__} executed in {end - start} sec")
        return res
    return decorator
