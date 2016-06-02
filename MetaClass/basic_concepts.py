print('http://python.jobbole.com/21351/')


'''
Class is also a object in python
'''
class ObjectCreator(object):
    pass

print(ObjectCreator)
ObjectCreator.version = 0.1
print(ObjectCreator.__dict__)
print(hasattr(ObjectCreator, 'version'))


'''
Dynamically create a class
'''
def choose_class(name):
    if name == 'foo':
        class Foo(object):
            pass
        return Foo
    else:
        class Bar(object):
            pass
        return Bar
MyClass = choose_class("foo")
foo = MyClass()
print(MyClass)
print(foo)

# use type to create
class MyShinyClass(object):
    pass
print(MyShinyClass.__dict__)
# which is equal to
MyShinyClass = type("MyShinyClass", (), {})
print(MyShinyClass.__dict__)

# another example
class Foo(object):
    bar = True
print(Foo.__dict__)
Foo = type("Foo", (), {"bar": True})
print(Foo.__dict__)
f = Foo()
print(f)

class FooChild(Foo):
    pass
print(FooChild.bar)
# which is equal to
FooChild = type("FooChild", (Foo, ), {})
print(FooChild.bar)

# add a function to class
def echo_bar(self):
    print(self.bar)

FooChild = type('FooChild', (Foo, ), {'echo_bar': echo_bar})
print(hasattr(FooChild, 'echo_bar'))
foo_child = FooChild()
foo_child.echo_bar()
print(foo_child.bar)


'''
MetaClass is the class used to create class
MetaClass is used to change the Class when creating them
'''

# __class__
class Bar(object):
    pass
bar = Bar()
print(bar.__class__)
print(bar.__class__.__class__)

# __metaclass__
class Foo(Bar):
    pass
# python will search for the __metaclass__ from Foo.
# if not found, then Bar, until the furthest super class
# if still not found, will search the module
# if not found, will use type to create Class object
#
# __metaclass__ can be type or subclass of type

# customize __metaclass__
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    attrs = ((name, value) for name, value in future_class_attr.items if not name.startswith('__'))
    upper_case_attrs = dict(((name.upper(), value) for name, value in attrs))
    return type(future_class_name, future_class_parents, upper_case_attrs)


__metaclass__ = upper_attr


class Foo(object):
    bar = 'bip'

print(hasattr(Foo, 'bar'))
print(hasattr(Foo, 'BAR'))
f = Foo()
#print(f.BAR)
