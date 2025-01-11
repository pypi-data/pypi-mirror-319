
def func():
    return "xyz's func"

def test_abc_func():
    from other_package.abc import func as abc_func
    return f"{func()} calling {abc_func()}"