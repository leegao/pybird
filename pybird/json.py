class jsonlist(object):
    
    final = True
    def __init__(self, set_):
        if isinstance(set_, (list, dict, tuple)): self.final = False
        self.obj = set_
    
    def __getattr__(self, name):
        if name in self.__dict__.keys():
            return self.__dict__[name]
        if name in self.__dict__['obj'].keys():
            if not self.final:
                return jsonlist(self.__dict__['obj'][name])
            else:
                return self.__dict__['obj'][name]
    def __str__(self):
        return str(self.obj)
        pass
    def keys(self):
        return self.obj.keys()
    def __getitem__(self, key):
        return self.obj[key]
    def __iter__(self):
        return iter(self.obj)