import logging
import timeit

task3_logger = logging.getLogger(__name__)
task3_logger.setLevel(logging.DEBUG)

task3_formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')

task3_file_handler = logging.FileHandler('log.txt')
task3_file_handler.setFormatter(task3_formatter)

task3_logger.addHandler(task3_file_handler)

def log_file(func):
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k} = {v!r}" for k,v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        task3_logger.debug(f"Calling {func.__name__}({signature})")
        res = func(*args, **kwargs)
        t = timeit.Timer(lambda: func(*args, **kwargs))
        time_taken = t.timeit(10000)
        task3_logger.debug(f"{func.__name__} returned {res!r} in {time_taken!r} seconds")
        return res
    return wrapper


@log_file
def my_func(n):
    ad = 0
    for v in range(n):
        ad = ad + v
    
    return ad

@log_file
def fib_func(num, kw=1, kw2="something"):
    fib = [0, 1]
    for i in range(2, num):
        fib.append(fib[i - 1] + fib[i - 2])
    return fib

@log_file
def jkl(name, pay=0, *args, **kwargs):
    pass

my_func(5)
fib_func(5)
jkl("ath", 10, 3, 6, a=9)
