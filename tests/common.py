import functools


def parametrized(param_list):
    """
    Decorates a test case to run it as a set of subtests.

    Credits: https://stackoverflow.com/a/62476654
    """

    def decorator(f):
        @functools.wraps(f)
        def wrapped(self):
            for param in param_list:
                with self.subTest(**param):
                    f(self, **param)

        return wrapped

    return decorator