import logging
import os
import traceback
import functools

__logFormatter__ = logging.Formatter("%(asctime)-19.19s [%(levelname)s] [%(threadName)s] %(message)s")
__qlogger__ = None 
__handlers__=dict()
__logpath__='qlog.log'
__loglevel__ = logging.DEBUG
__consoleOutput__ = True
__fileHandler__ = None
__consoleHandler__ = None
__line__ = '*'*40
def __createFileHandler__():
    global __fileHandler__
    __fileHandler__= logging.FileHandler(__logpath__)
    __fileHandler__.setFormatter(__logFormatter__)
    __fileHandler__.setLevel(__loglevel__)    

def __createConsoleHandler__():
    global __consoleHandler__
    __consoleHandler__ = logging.StreamHandler()
    __consoleHandler__.setFormatter(__logFormatter__)
    __consoleHandler__.setLevel(__loglevel__)

def __createLogDir__(path):
    path = os.path.abspath(path)
    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.isdir(os.path.dirname(path)))

def init(path='qlog.log',level=logging.DEBUG):    
    global __qlogger__
    global __loglevel__
    global __handlers__
    
    __qlogger__ = logging.getLogger('qlog')
    __qlogger__.handlers=[]
    __qlogger__.setLevel(__loglevel__)

    __createLogDir__(path)
    __logpath__= path
    __loglevel__= level
    __handlers__={}
    __qlogger__.handlers=[]
    __qlogger__.setLevel(__loglevel__)
    __createFileHandler__()
    __handlers__['file']=__fileHandler__
    __qlogger__.addHandler(__fileHandler__)
    __createConsoleHandler__()
    __handlers__['console']=__consoleHandler__
    __qlogger__.addHandler(__consoleHandler__)
    
def getLogger(name):
    if name=='qlog':
        return __qlogger__
    else:
        return logging.getLogger(name)
    
def enterleave(level = logging.DEBUG,rethrow=True,loggername='qlog'):
    def enterleave_wrap(func):
        @functools.wraps(func)
        def func_warp(*args, **kwargs):            
            try:
                if level>=__loglevel__:
                    qlog_msg='[ENTER]%s(%s)'%(func.__name__,str(args) + str(kwargs))
                    getLogger(loggername).log(level,qlog_msg)
                return_val = func(*args, **kwargs)                
                if level>=__loglevel__:
                    qlog_msg = '[RETURN]%s(%s)'%(func.__name__,return_val)
                    getLogger(loggername).log(level,qlog_msg)
                return_val
            except Exception as ex:
                #tb = traceback.format_exc()
                qlog_msg = '[RAISE]%s: %s'%(func.__name__,ex)
                getLogger(loggername).error(qlog_msg)
                if rethrow:
                    raise ex
        return func_warp
    return enterleave_wrap

def ex(level = logging.ERROR,rethrow=False,loggername='qlog'):    
    def ex_wrap(func):
        @functools.wraps(func)
        def func_warp(*args, **kwargs):            
            try:
                return_val = func(*args, **kwargs)
                return return_val
            except Exception as ex:
                if level>=__loglevel__:
                    #tb = traceback.format_exc()
                    qlog_msg = '[RAISE]%s: %s'%(func.__name__,ex)
                    getLogger(loggername).error(qlog_msg)
                if rethrow:
                    raise ex            
        return func_warp
    return ex_wrap

def trace(level = logging.ERROR,rethrow=False,loggername='qlog'):
    def trace_wrap(func):
        @functools.wraps(func)
        def func_warp(*args, **kwargs):            
            try:
                return_val = func(*args, **kwargs)
                return return_val
            except Exception as ex:
                if level>=__loglevel__:
                    tb = traceback.format_exc()                    
                    qlog_msg = f'[RAISE]{func.__name__}\n{__line__}TRACE START{__line__}\n{tb}\n{__line__}TRACE END{__line__}\n'
                    getLogger(loggername).error(qlog_msg)
                if rethrow:
                    raise ex            
        return func_warp
    return trace_wrap

def setLogger(logger):
    __qlogger__ = logger

def setLogPath(new_path):
    __createLogDir__(new_path)
    __logpath__ = new_path     
    __createFileHandler__()
    __handlers__['file']=__fileHandler__
    __initHandlers__()

def setConsole(output=True):
    __consoleOutput__ = output
    __initHandlers__()

def __initHandlers__():   
    handlers=['file'] 
    if __consoleOutput__:
        handlers.append('console')
    __qlogger__.handlers=[]
    for name in handlers:
        __qlogger__.addHandler(__handlers__[name])
    

init()
