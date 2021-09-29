from qqlog import ex,init,enterleave,trace
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

import logging
logging.getLogger('newlogger')

@enterleave(loggername='newlogger',level=logging.ERROR)
def new_logger_test(a,b):
    return a+b

try:
    test1(1,0)
    test2(1,1)
    test3(1,0)
    test4(1,2,prefix='result:')
    df_test(1,2,df)
    np_test(1,2,d)
    testclass().sum(10,20)
    new_logger_test(5,15)
    
    
except Exception as ex:
    print(ex)