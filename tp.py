import functools
import timeit


def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #something before
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k} = {v!r}" for k,v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        res = func(*args, **kwargs)
        t = timeit.Timer(lambda: func(*args, **kwargs))
        time_taken = t.timeit(100000)
        print(f"{func.__name__} returned {res!r} in {time_taken!r} seconds")
        #something after  {time_taken!r}
        return res
    return wrapper

@my_decorator
def my_func(n):
    ad = 0
    for v in range(n):
        ad = ad + v
    
    return ad

my_func(15)

