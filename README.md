# qqlog install
```python
pip install qqlog
```

# qqlog example

```python
from qqlog import ex,init,enterleave,trace
import logging
# init(path='./log/qqlog.log',level=logging.DEBUG)
init()
@ex()
def test1(a,b):
    return a/b

@enterleave()
def test2(a,b):
    return a/b    

@trace()
def test3(a,b):
    return a/b

try:
    test1(1,0)
    test2(1,1)
    test3(1,0)
except Exception as ex:
    print(ex)

```
# Console/qqlog.log
```
2021-09-26 14:00:04 [ERROR] [MainThread] [RAISE]test1: division by zero
2021-09-26 14:00:04 [DEBUG] [MainThread] [ENTER]test2((1, 1){})
2021-09-26 14:00:04 [DEBUG] [MainThread] [RETURN]test2(1.0)
2021-09-26 14:00:04 [ERROR] [MainThread] [RAISE]test3
****************************************TRACE START****************************************
Traceback (most recent call last):
  File "E:\jupyter\projects\whl\qqlog\qqlog\__init__.py", line 104, in func_warp
    return_val = func(*args, **kwargs)
  File "E:\jupyter\projects\whl\qqlog\example.py", line 16, in test3
    return a/b
ZeroDivisionError: division by zero

****************************************TRACE END****************************************
```