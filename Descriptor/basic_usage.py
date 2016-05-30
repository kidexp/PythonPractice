print("descriptor example")

'''
Assume we have an instance a, to access a.x, the order of how python access that:
    * object attribute a.__dict__['x'],
    * class attribute type(a).__dict__['x']
    * parent class

Descriptor is only valid for class inherits from type or object, and implements one of __get__, __set__ and __delete__
functions.

Descriptor protocol:
    * __get__
    * __set__
    * __delete__

Read-only data descriptor:
    * __get__
    * __set__: throw AttributeError
'''

class WebFramework(object):

    def __init__(self, name="Flask"):
        self.name = name

    '''
    data descriptor: implements both __get__ and __set__
    '''

    def __get__(self, instance, owner):
        return self.name

    def __set__(self, instance, value):
        self.name = value

class PythonSite(object):

    web_framework = WebFramework()

print(PythonSite.web_framework)
PythonSite.web_framework = "Tornado"
print(PythonSite.web_framework)



'''
How to use descriptor
'''

web_framework = WebFramework()
print(web_framework.__get__(web_framework, WebFramework))
print(web_framework.__dict__['name'])


'''
Descriptor, object attributes, instance attributes
'''
class PythonSite(object):

    web_framework = WebFramework()
    version = 0.01

    def __init__(self, site):
        self.site = site

python_site = PythonSite('ghost')
print(vars(PythonSite).items())
print(vars(python_site))
print(PythonSite.__dict__)


python_site1 = PythonSite('ghost')
python_site2 = PythonSite('admin')
print('PythonSite version : {version}'.format(version=PythonSite.version))
print('python_site1 version: {version}'.format(version=python_site1.version))
print('python_site2 version: {version}'.format(version=python_site2.version))
print(python_site1.version is python_site2.version)
python_site1.version = "python_site1"
print(python_site1.__dict__)
print(python_site2.__dict__)
PythonSite.version = 0.02
print(python_site1.version)
print(python_site2.version)


'''
Instance method, class method, static method and descriptor

When get descriptor it actually calls object.__getattribute__():
    * object: type(obj).__dict['x'].__get__(obj, type(obj))
    * class: type(class).__dict['x'].__get__(None, type(class))
'''
class PythonSite(object):

    web_framework = WebFramework()
    version = 0.01

    def __init__(self, site):
        self.site = site

    def get_site(self):
        # instance method is unbound in class
        return self.site

    @classmethod
    def get_version(cls):
        # class method needs take the cls as input of the parameter
        return cls.version

    @staticmethod
    def find_version():
        # static method has to use the class name in order to access its member
        return PythonSite.version

ps = PythonSite('ghost')
print(ps.get_version())
print(PythonSite.get_version())
print(type(ps).__dict__['get_version'].__get__(ps, type(ps)) == PythonSite.__dict__['get_version'].__get__(None, PythonSite))
print(type(ps) is PythonSite)


print(type(ps).__dict__['get_site'].__get__(ps, type(ps)))
print(PythonSite.__dict__['get_site'].__get__(ps, PythonSite))
print(PythonSite.__dict__['get_site'].__get__(None, PythonSite))


'''
Application of descriptor
'''
class _Missing(object):
    def __repr__(self):
        return 'no value'

    def __reduce__(self):
        return '_missing'

_missing = _Missing()

class cache_property(object):
    def __init__(self, func, name=None, doc = None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __get__(self,  obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value

class Foo(object):
    @cache_property
    def foo(self):
        print('first calculate')
        result = 'this is result'
        return result

f = Foo()
print(f.foo)
print(f.foo)
