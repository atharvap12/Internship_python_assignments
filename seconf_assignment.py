#Task 1 : Implement a stack using list.

class my_stack:
    def __init__(self):
        self.lis = []

    def push_stack(self, num):
        self.lis.append(num)
        print("Pushed Successfully.")

    def pop_stack(self):
        print("Popped Successfully.")
        print(self.lis.pop())

    def is_empty(self):
        if len(self.lis) == 0:
            print("Stack is empty")
        else:
            print("Stack is not empty")

    def size(self):
        sl = len(self.lis)
        print(f"Stack size:{sl}")

    def print_stack(self):
        for e in self.lis:
            print(str(e) + " ")

stck = my_stack()
print("Stack Object Created.")
while True:

    print("Press 1 to push to the stack")
    print("Press 2 to pop from the stack")
    print("Press 3 to know if the stack is empty")
    print("Press 4 to get the size of the stack")
    print("Press 5 to print the stack")
    print("Press 6 to exit")
    ip = int(input("Enter your input:"))

    if ip == 1:
        v = int(input("Enter the integer input:"))
        stck.push_stack(v)
    elif ip == 2:
        stck.pop_stack()
    elif ip == 3:
        stck.is_empty()
    elif ip == 4:
        stck.size()
    elif ip == 5:
        stck.print_stack()
    elif ip == 6:
        print("Exiting.")
        break
    else:
        print("Invalid Input")