# helpers.py


from typing import Any, Iterable


def allowed(obj, black_list=None, white_list=None) -> bool:
    """Helper: general check if an object mathes both black & white list (assume no restriction if related list is empty)"""
    if black_list and obj in black_list:
        return False
    if white_list and obj not in white_list:
        return False
    return True


class CallWrapper:
    """ Helper class: wrapper over function or method call, somewhat like functools.partial(). 
        The first argument of unbound method ('self', 'this' object) can be set & changed any time.
    """
    def __init__(self, func, args=(), kwargs=None, this=None) -> None:
        self.func = func # function or method
        self.args = args
        self.kwargs = kwargs or {}
        self.this = this  # object to call the method on
    def with_this(self, this=None):
        self.this = this
        return self
    def call_as_function(self, *more_args, **more_kwargs) -> Any:
        """ Use also for bound methods. """
        all_kwargs = {**self.kwargs, **(more_kwargs)}
        return self.func(*self.args, *more_args, **all_kwargs)
    def call_as_method(self, *more_args, **more_kwargs) -> Any:
        """ Use for unbound methods. """
        all_kwargs = {**self.kwargs, **(more_kwargs)}
        return self.func(self.this, *self.args, *more_args, **all_kwargs)
    def call(self, *more_args, **more_kwargs) -> Any:
        if self.this:
            self.call_as_method(*more_args, **more_kwargs)
        else:
            self.call_as_function(*more_args, **more_kwargs)

    __call__ = call



def recursive_dive_along_attribute(obj, attr_name: str) -> Iterable:
    """ Recursive depth-first traversal of objects, searching for a specified attribute within an attribute's value or the elements of an iterable within the attribute. """
    yield obj
    
    if not hasattr(obj, attr_name):
        return
    # `obj` is an object we need to inspect more
    
    attr_value = getattr(obj, attr_name)
    if hasattr(attr_value, attr_name):
        # just a field with similar object
        yield from recursive_dive_along_attribute(attr_value, attr_name)
    else:
        # this might be a container
        try:
            iterator = iter(attr_value)
        except TypeError:
            pass # not iterable; see https://stackoverflow.com/a/1952655/12824563
        else:
            # iterable
            for item in iterator:
                yield from recursive_dive_along_attribute(item, attr_name)


def id_generator():
    i = 0
    while True:
        i += 1
        yield i

# Locally unique ID generator. Usage: `my_id = next(UID)`.
UID = id_generator()
