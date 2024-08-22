def m1(**kwargs):
    print(kwargs)
    print(kwargs is None)


def m2(*args):
    print(args)
    print(args[0])
    print(args[1])
    print(args[2])


# m2(*[1, 2, 3])

print(bool('False'))
