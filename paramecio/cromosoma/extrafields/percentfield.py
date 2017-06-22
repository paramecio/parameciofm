from paramecio.cromosoma.corefields import IntegerField

class PercentField(IntegerField):
    
    def __init__(self, name, required=False):
        
        super().__init__(name, 2, required)

    def check(self, value):
        
        try:
            value=int(value)
            
            if value<0:
                value=0
            if value>100:
                value=100
            
        except:
            value=0

        return value
