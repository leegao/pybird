import urllib2
from base64 import b64encode
from urllib import urlencode
import simplejson as json


class request(object):
    
    data = {}
    headers = {}
    
    def __init__(self, username, password, agent = "pyBird.rc1", domain = "http://twitter.com/", format = 'json', method = "GET"):
        self.agent = agent
        
        self.username = username
        self.password = password
        
        self.domain = domain
        self.format = format
        
        self.method = method
        
        if username and password:
            self.basic_auth()
            
        self.request = urllib2.Request(self.domain)
        self.clean = True
    
    def add_header(self, name, header):
        self.headers[name] = header
    
    def add_data(self, name, data):
        self.data[name] = data
        
    def clear_data(self):
        self.data = {}
        
    def clear_headers(self):
        self.headers = {}
    
    def has_auth_info(self):
        if not "password" in self.__dict__.keys() or not "username" in self.__dict__.keys(): return False
        return True
    
    def basic_auth(self):
        if not self.has_auth_info(): return
        self.auth = "Basic %s" % b64encode("%s:%s" % (self.username, self.password))
        self.add_header("Authorization", self.auth)
    
    def set_agent(self):
        self.add_header("X-Twitter-Client", self.agent)
    
    def basic_headers(self):
        self.clear_headers()
        self.basic_auth()
        self.set_agent()
    
    def __setattr__(self, name, value):
        try:
            self.__dict__[name]= value
        finally:
            if name == "data":
                if not isinstance(value, dict): raise "Invalid Data"
            elif name == "headers":
                if not isinstance(value, dict): raise "Invalid Headers"
                self.basic_auth()
            elif name == "method":
                if not value in ("GET", "POST"): raise "Invalid Method"
            elif name in ("password", "username"):
                self.basic_headers()
        
    def __update__(self):
        self.clean = True
        self.basic_headers()
        self.clear_data()
        
    def __call__(self, resource = None, method = "GET", **kwargs):
        import resource as res
        
        if not self.clean:
            self.__update__()
        data = urlencode(self.data)
        
        if isinstance(resource, res.res) or isinstance(resource, res.rtuple):
            if resource.data:
                data += urlencode(resource.data)
            method = resource.method
            
        resource = str(resource)
        
        pstr = ''
        pdata = None
        
        if 'id' in kwargs.keys(): resource += '/%s'%kwargs['id']
        
        if method == "GET":
            pstr = "?%s%s"%(data, urlencode(kwargs))
        else:
            pdata = data + urlencode(kwargs)
        
        self.request = urllib2.Request("%s%s.%s%s" % (self.domain, resource, self.format, pstr),
                                       pdata, self.headers)
        self.clean = False
        try:
            ret = urllib2.urlopen(self.request)
        except urllib2.HTTPError, e:
            ret = e
        finally:
            return ret
