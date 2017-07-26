from paramecio.cromosoma.corefields import IntegerField
from paramecio.cromosoma.extraforms.colorform import ColorForm

class ColorField(IntegerField):

    def __init__(self, name, size=11, required=False):
        super().__init__(name, size, required)
        
        self.name_form=ColorForm
    
    def check(self, value):
        
        value=str(value).replace('#', '0x')
        
        value=int(value, 16)
        
        if value<0 or value>0xffffff:
            value=0
            
        return value
    def get_hex_color(self, value):
        
        value=str(hex(int(value))).replace('0x', '')
        
        c=len(value)
        
        if(c<6):
            repeat=6-c
            value=('0'*repeat)+value
            
        value='#'+value
        
        return value

    def show_formatted(self, value):

        value=str(hex(int(value))).replace('0x', '')
        
        c=len(value)
        
        if(c<6):
            repeat=6-c
            value=('0'*repeat)+value
            
        value='#'+value

        return '<div style="width:50px;height:50px;background-color:%s;"></div>' % value;
