#lists and tuples
fruits = ["apple", "banana", "orange", "grape"]
fruits.append("watermelon")
print(len(fruits))

colors = ("red", "green", "blue")
print(colors[1])

#dictionaries and sets
student = {"name":"atharva puranik", "age":20, 
    "university":"vishwakarma institute of information technology"}

print(student["age"])

skills = {"communication", "technical", "decision-making"}
skills.add("negotiation")
print(len(skills))

#data structures and functions
class Book:
    def __init__(self, title_val, author_val, year_val):
        self.title_ = title_val
        self.author = author_val
        self.year = year_val


Book("A crime thriller", "Byomkesh Bakshi", 1980)

def print_book_info(book_obj):
    print(book_obj.title_)
    print(book_obj.author)
    print(book_obj.year)

#itertools
import itertools

numbers = [1, 2, 3]
perm = itertools.permutations(numbers)
print(type(perm))
for v in list(perm):
    print(v)

#decorators
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
        time_taken = timeit.timeit(func, number=10000)
        print(f"{func.__name__} returned {res!r} in {time_taken!r} seconds")
        #something after  {time_taken!r}
        return res
    return wrapper

@my_decorator
def my_func():
    ad = 0
    for v in range(100):
        ad = ad + v
    
    return ad

my_func()