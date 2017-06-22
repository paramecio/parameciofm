from paramecio.cromosoma.corefields import FloatField
from decimal import Decimal, getcontext
from locale import format

getcontext().prec=2

class MoneyField(FloatField):
    
    def __init__(self, name, required=False):
        
        super().__init__(name, 11, required)

    def check(self, value):
        
        value=Decimal(value)

        return value

    def show_formatted(self, value):
        
        return format('%.2f', Decimal(value), grouping=True)

    @staticmethod
    def format_money(value):
        return format('%.2f', Decimal(value), grouping=True)        

