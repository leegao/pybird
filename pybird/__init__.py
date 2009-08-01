from request import *
from resource import *
from json import jsonlist
import simplejson as json


Status = status()
Account = account()

class birdie(object):
    
    def __init__(self, username = None, password = None, format = 'json'):
        self.req = request(username = username, password = password, format = format)
        self.engines = {
                       'json':jsonlist,
                       'xml':None,
                       }
        self.engine = self.engines[format]
    
    def login(self, username, password):
        self.req.username = username
        self.req.password = password
    
    def format(self, format):
        self.req.format = format
        self.engine = self.engines[format]
    def read(self, resource):
        opener = self.req(resource)
        try:
            return opener.read()
        except:
            print opener.code
            return None
    def __call__(self, resource):
        try:
            return self.engine(json.loads(self.req(resource).read()))
        except:
            return None
     
Birdie = birdie()