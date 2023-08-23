class DataSerializer:
    def __init__(self,instance,*args, **kwargs):
        self.instance = instance
        self.many = kwargs.get('many')
    
    def to_representation(self,*args, **kwargs):
        if not self.many:
            return self.instance.data
        return list(map(lambda x: x.data,self.instance))
    
    @property
    def data(self):
        return self.to_representation()