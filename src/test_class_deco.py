from math import exp
import time
import functools
import random


def deco(func):
    print("run deco 1 enter__")
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        print("run deco1 wrapped")
        return func(*args, **kwargs)
    print("run deco 1 exit__")
    return wrapped

def deco2(func):
    print("run deco 2 enter__")
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        print("run deco2 wrapped")
        return func(*args, **kwargs)
    print("run deco 2 exit__")
    return wrapped

class Sample:
    testint = 100
    def __init__(self):
        pass

    @deco2
    @deco
    def say(self, mount: int) -> None:
        print("haha"+str(mount))

    
    def main(self):
        self.say(10)


if __name__=="__main__":
    try:
        Sample().main()
    except BaseException:
        pass