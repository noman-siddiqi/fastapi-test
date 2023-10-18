# def add(x, y):
#     return x+ y
    
# def sub(x, y):
#     return x - y
    
# def abcd(func, x, y):
#     val = func(x, y) 
#     print(val)     
    
# print(add(3, 4))  
# val = add
# print (val(4,5))  

# abcd(add, 6,4)
# abcd(sub, 8,4)


# def msg(fname, lname):
#     full_name = f"{fname} {lname}"
#     print(full_name)
#     def welcome(full_name):
#         return f"Hello {full_name}!"
#     return welcome


# val = msg('Noman', 'Siddiqi')
# print(val)


# def cdef(msg, func):
    
#     def message():
#         print(msg)
#         func()
#     return message()   


# def testing():
#     print('Hello print testing')
        

# val = cdef("Welcome", testing)      


def hello(func):
    
    def message():
        print('Welcome')
        func()
    return message()   

@hello
def testing():
    print('Hello print testing')
    
testing