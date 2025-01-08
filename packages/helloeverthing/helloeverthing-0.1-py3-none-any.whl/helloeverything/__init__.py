import os

def HelloWorld():
    print("Hello, World!")

def HelloName(name):
    print(f"Hello,{name}!")

def HelloUser():
    print(f"Hello, {os.getlogin()}!")