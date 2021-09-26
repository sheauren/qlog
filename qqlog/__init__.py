import logging
import os
import traceback
import functools
from uuid import uuid4

__logFormatter__ = logging.Formatter("%(asctime)-19.19s [%(levelname)s] [%(threadName)s] %(message)s")
__qqlogger__ = None 
__handlers__=dict()
__logpath__='qqlog.log'
__loglevel__ = logging.DEBUG
__consoleOutput__ = True
__fileHandler__ = None
__consoleHandler__ = None
__line__ = '*'*40
__dirs__=dict()
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

def init(path='qqlog.log',level=logging.DEBUG):    
    global __qqlogger__
    global __loglevel__
    global __handlers__
    
    __qqlogger__ = logging.getLogger('qqlog')
    __qqlogger__.handlers=[]
    __qqlogger__.setLevel(__loglevel__)

    __createLogDir__(path)
    __logpath__= path
    __loglevel__= level
    __handlers__={}
    __qqlogger__.handlers=[]
    __qqlogger__.setLevel(__loglevel__)
    __createFileHandler__()
    __handlers__['file']=__fileHandler__
    __qqlogger__.addHandler(__fileHandler__)
    __createConsoleHandler__()
    __handlers__['console']=__consoleHandler__
    __qqlogger__.addHandler(__consoleHandler__)
    
def getLogger(name):
    if name=='qqlog':
        return __qqlogger__
    else:
        return logging.getLogger(name)

def dtypeToStr(t,v):
    global __dirs__
    if t =='str':
        return t,"'%s'"%v
    elif t in ['int','float','complex','dict','set','bool']:
        return t,str(v)        
    elif t in ['bytes', 'bytearray', 'memoryview']:
        return t,str(v)        
    elif t =='DataFrame':
        try:            
            if 'dataframe' not in __dirs__:
                dataframe_dir = os.path.join(os.path.dirname(__logpath__),'dataframe')
                __dirs__['dataframe'] = dataframe_dir            
                if not os.path.isdir(dataframe_dir):
                    os.makedirs(dataframe_dir)
            else:
                dataframe_dir = __dirs__['dataframe']
            id = uuid4()
            csv_path = os.path.join(dataframe_dir,f'{id}.csv')            
            v.to_csv(csv_path,index=False)
        except Exception as ex:
            print(ex)            
        return t,f'[{id}.csv]'
    elif t =='ndarray': # numpy ndarray
        try:
            if 'ndarray' not in __dirs__:
                ndarray_dir = os.path.join(os.path.dirname(__logpath__),'ndarray')
                __dirs__['ndarray'] = ndarray_dir            
                if not os.path.isdir(ndarray_dir):
                    os.makedirs(ndarray_dir)
            else:
                ndarray_dir = __dirs__['ndarray']
            id = uuid4()
            ndarray_path = os.path.join(ndarray_dir,f'{id}.txt')            
            v.tofile(ndarray_path, sep=' ', format='%s')
        except Exception as ex:
            print(ex)
        return t,f'[{id}.ary]'

def formatParams(*args, **kwargs):    
    # params = ['%d:%s=`%s`'%(i,type(v).__name__,str(v)) for i,v in enumerate(args)]+["%s:%s=`%s`"%(key,type(val).__name__,str(val)) for key,val in kwargs.items()]
    params = []
    for i,v in enumerate(args):
        t = type(v).__name__
        t,v = dtypeToStr(t,v)
        params.append(f'{i}:{t}={v}')
    for k,v in kwargs.items():
        t = type(v).__name__
        t,v = dtypeToStr(t,v)
        params.append(f'{k}:{t}={v}')
    return params

def enterleave(level = logging.DEBUG,rethrow=True,loggername='qqlog'):
    def enterleave_wrap(func):
        @functools.wraps(func)
        def func_warp(*args, **kwargs):            
            try:
                if level>=__loglevel__:
                    params = formatParams(*args,**kwargs)
                    qqlog_msg='[ENTER]%s(%s)'%(func.__name__,', '.join(params))
                    getLogger(loggername).log(level,qqlog_msg)
                return_val = func(*args, **kwargs)                
                if level>=__loglevel__:
                    qqlog_msg = '[RETURN]%s(%s)'%(func.__name__,return_val)
                    getLogger(loggername).log(level,qqlog_msg)
                return_val
            except Exception as ex:
                #tb = traceback.format_exc()
                qqlog_msg = '[RAISE]%s: %s'%(func.__name__,ex)
                getLogger(loggername).error(qqlog_msg)
                if rethrow:
                    raise ex
        return func_warp
    return enterleave_wrap

def ex(level = logging.ERROR,rethrow=False,loggername='qqlog'):    
    def ex_wrap(func):
        @functools.wraps(func)
        def func_warp(*args, **kwargs):            
            try:
                return_val = func(*args, **kwargs)
                return return_val
            except Exception as ex:
                if level>=__loglevel__:
                    #tb = traceback.format_exc()
                    qqlog_msg = '[RAISE]%s: %s'%(func.__name__,ex)
                    getLogger(loggername).error(qqlog_msg)
                if rethrow:
                    raise ex            
        return func_warp
    return ex_wrap

def trace(level = logging.ERROR,rethrow=False,loggername='qqlog'):
    def trace_wrap(func):
        @functools.wraps(func)
        def func_warp(*args, **kwargs):            
            try:
                return_val = func(*args, **kwargs)
                return return_val
            except Exception as ex:
                if level>=__loglevel__:
                    tb = traceback.format_exc()                    
                    qqlog_msg = f'[RAISE]{func.__name__}\n{__line__}TRACE START{__line__}\n{tb}\n{__line__}TRACE END{__line__}\n'
                    getLogger(loggername).error(qqlog_msg)
                if rethrow:
                    raise ex            
        return func_warp
    return trace_wrap

def setLogger(logger):
    __qqlogger__ = logger

def setLogPath(new_path):    
    global __logpath__
    global __dirs__
    global __handlers__
    __logpath__ = new_path
    __dirs__ = []
    if __logpath__ is not None:
        __createLogDir__(new_path)
        __createFileHandler__()
        __handlers__['file']=__fileHandler__
    __initHandlers__()

def setConsole(output=True):
    global __consoleOutput__
    __consoleOutput__ = output
    __initHandlers__()

def __initHandlers__():
    global __logpath__
    global __consoleOutput__
    global __qqlogger__
    global __handlers__
    if __logpath__ is None:  
        handlers=[]
    else:
        handlers=['file'] 
    if __consoleOutput__:
        handlers.append('console')
    __qqlogger__.handlers=[]
    for name in handlers:
        __qqlogger__.addHandler(__handlers__[name])
    

init()
