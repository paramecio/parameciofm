#!/usr/bin/env python3

from paramecio.cromosoma.coreforms import BaseForm
from paramecio.citoplasma.mtemplates import standard_t
from paramecio.citoplasma.datetime import format_timedata

class DateForm(BaseForm):
    
    def __init__(self, name, value):
        
        super().__init__(name, value)
        
        self.yes_time=False

    def form(self):
        
        y=''
        m=''
        d=''
        h=''
        min=''
        s=''
        
        time=format_timedata(self.default_value)
        
        if time==True:
            y=int(time[0])
            m=int(time[1])
            d=int(time[2])
            h=int(time[3])
            min=int(time[4])
            s=int(time[5])

        return standard_t.load_template('forms/dateform.phtml', yes_time=self.yes_time, form=self.name, y=y, m=m, d=d, h=h, min=min, s=s)

    #def 
                         