
# qqlog install
```python
pip install qqlog
```

# qqlog example

```python
from qqlog import ex,init,enterleave,trace
#import logging
init()
#init(path='./log/qqlog.log',level=logging.DEBUG)

@ex()
def test1(a,b):
    return a/b

@enterleave()
def test2(a,b):
    return a/b    

@trace()
def test3(a,b):
    return a/b

@enterleave()
def test4(a,b,prefix='answer is'):
    val = a/b
    print('%s %s'%(prefix,str(val)))
    return val

class testclass(object):
    @enterleave()
    def __init__(self):
        print('init')
    @enterleave()
    def sum(self,a,b):
        return a+b

import pandas as pd
df = pd.DataFrame(data={'1':[1,2,3],'b':['test1','test2','test3']},index=range(3))

@enterleave()
def df_test(a,b,df):
    val = a+b+df['1'].sum()    
    return val

import numpy as np
d = np.array([[1,2,3],[4,5,6]])

@enterleave()
def np_test(a,b,d):
    val = a+b+d.sum()    
    return val

try:
    test1(1,0)
    test2(1,1)
    test3(1,0)
    test4(1,2,prefix='result:')
    df_test(1,2,df)
    np_test(1,2,d)
    testclass().sum(10,20)
except Exception as ex:
    print(ex)

```
# Console/qqlog.log
```
2021-09-27 21:10:31 [ERROR] [MainThread] [RAISE]test1: division by zero
2021-09-27 21:10:31 [DEBUG] [MainThread] [ENTER]test2(0:int=1, 1:int=1)
2021-09-27 21:10:31 [DEBUG] [MainThread] [RETURN]test2(1.0)
2021-09-27 21:10:31 [ERROR] [MainThread] [RAISE]test3
****************************************TRACE START****************************************
Traceback (most recent call last):
  File "E:\jupyter\projects\whl\qqlog\qqlog\__init__.py", line 173, in func_warp
    return_val = func(*args, **kwargs)
  File ".\example.py", line 16, in test3
    return a/b
ZeroDivisionError: division by zero

****************************************TRACE END****************************************

2021-09-27 21:10:31 [DEBUG] [MainThread] [ENTER]test4(0:int=1, 1:int=2, prefix:str='result:')
result: 0.5
2021-09-27 21:10:31 [DEBUG] [MainThread] [RETURN]test4(0.5)
2021-09-27 21:10:31 [DEBUG] [MainThread] [ENTER]df_test(0:int=1, 1:int=2, 2:DataFrame=[74781786-7b2a-437d-a4f8-0ed1aea4d412.csv])
2021-09-27 21:10:31 [DEBUG] [MainThread] [RETURN]df_test(9)
2021-09-27 21:10:31 [DEBUG] [MainThread] [ENTER]np_test(0:int=1, 1:int=2, 2:ndarray=[fc36566c-e1b8-46e3-a90f-e02b690c6234.ary])2021-09-27 21:10:31 [DEBUG] [MainThread] [RETURN]np_test(24)
2021-09-27 21:10:31 [DEBUG] [MainThread] [ENTER]__init__()
init
2021-09-27 21:10:31 [DEBUG] [MainThread] [RETURN]__init__(None)
2021-09-27 21:10:31 [DEBUG] [MainThread] [ENTER]sum(0:int=10, 1:int=20)
2021-09-27 21:10:31 [DEBUG] [MainThread] [RETURN]sum(30)
```

