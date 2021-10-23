from qqlog import ex,init,createCsvFileLogger,createConsoleFileLogger
import logging
init()

createCsvFileLogger('csv',level=logging.DEBUG,headers=['asctime','funcName','levelname','msg'],formatters=['asctime','funcName','levelname','msg'],path='debug.csv')
createConsoleFileLogger('consolefile',level=logging.DEBUG,path='./consolefile.log')

@ex(loggername='csv',rethrow=False)
def test_csv(a,b):
    return a/b

@ex(loggername='consolefile',rethrow=False)
def test_consolefile(a,b):
    return a/b

try:
    test_csv(1,0)
    test_consolefile(1,0)
except Exception as ex:
    print(ex)