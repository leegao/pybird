from copy import copy
class KEY(object):
    pass

class OBJ(object):
    pass

class OPT(object):
    pass

class rtuple(object):
    def __init__(self, *args):
        self.data = args[1]
        self.str_ = args[0]
        self.method = args[2]
    def __str__(self):
        return str(self.str_)
    def __add__(self, other):
        return self.str_ + other
    def __radd__(self, other):
        return other + self.str_
    def get_data(self):
        return self.data

class resource(object):    
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self.__dict__[key] = kwargs[key]
    
    def __getattr__(self, name):
        if name not in self.__dict__.keys():
            return None
        var = self.__dict__[name]
        if isinstance(var, url):
            return var.url


class res(object):
    def __init__(self, url = '', k = 'k', **kwargs):
        if isinstance(url, dict):
            self.url = url.pop('url')
            kwargs = url
        else:
            self.url = url
        self.k = k
        self.method = 'GET'
        self.callback = None
        self.key = None
        
        if 'method' in kwargs.keys():
            self.method = kwargs['method']
            kwargs.pop('method')
        if 'call' in kwargs.keys():
            self.call = kwargs['call']
            kwargs.pop('call')
        if 'callback' in kwargs.keys():
            self.callback = kwargs['callback']
            kwargs.pop('callback')
        
        self.args = kwargs    
        
        n = 0
        for key in kwargs.keys():
            val = kwargs[key]
            self.__dict__[key] = kwargs[key]
            if val == KEY:
                self.key = key
            elif val == OBJ:
                n+=1
        self._len = n
                
    def __getattr__(self, name):
        if not name in self.__dict__.keys():
            if name[0:len(self.k)] != self.k: return None
            #Invoke transformation with key
            if not 'call' in self.__dict__.keys():
                return None
            call = self.__dict__['call']
            if len(call) > 1:
                return None
            return rtuple(self.__dict__['url'] + "/%s" % name[len(self.k):], {self.key:name[len(self.k):]}, self.method)
            
        return self.__doc__[name]
    
    def __str__(self):
        return self.url
    def __add__(self, other):
        return self.url + other
    def __radd__(self, other):
        return other + self.url
    
    def __call__(self, key = None, **k):
        url = self.url
        if self.key in k.keys():
            key = k.pop(self.key)
        if not key: self.url
        
        if len(k) < self._len: return None
        
        for _k in k.keys():
            if _k not in self.args.keys(): return None
        
        if 'call' in self.__dict__.keys():
            call = self.__dict__['call']
            url += '/%s'*len(call)
            _call = []
            for c in call:
                if self.args[c] == KEY: _call.append(key)
                else: _call.append(k[c])
            _call = tuple(_call)
            url = url % _call
        
        k[self.key] = key
        
        return rtuple(url, k, self.method)
    
class status(resource):
    show = res(
               url = 'statuses/show',
               method = 'GET',
               call = ['id'],
               
               id = KEY,
               )
    update = res(
                 url = 'statuses/update',
                 method = 'POST',
                 
                 status = KEY,
                 in_reply_to_status_id = OPT
                 )
    destroy = res(
                  url = 'statuses/destroy',
                  method = 'POST',
                  call = ['id'],

                  id = KEY,
                  )
    
class account(resource):
    verify_credentials = res(
                             url = 'account/verify_credentials'
                             )