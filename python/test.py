import functools

def bar(show):
    if show:
        print('bar')
    def param_fuc(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper
    return param_fuc

def inject(show):
    

class Foo:
    show = True

    def __init__(self):
        self.foo
        pass

    @bar
    def foo(self):
        print('foo')


Foo().foo()
