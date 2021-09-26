from qlog import ex,init,enterleave,trace
#import logging
init()
#init(path='./log/qlog.log',level=logging.DEBUG)

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