#!/usr/bin/env python3

from paramecio.cromosoma.coreforms import BaseForm
from paramecio.citoplasma.mtemplates import standard_t
from paramecio.citoplasma.datetime import format_timedata

class DateForm(BaseForm):
    
    def __init__(self, name, value):
        
        super().__init__(name, value)
        
        self.yes_time=False
        self.t=standard_t

    def form(self):
        
        y=''
        m=''
        d=''
        h=''
        min=''
        s=''
        min_time=''
        
        time=format_timedata(self.default_value)
        
        if time[0]:
            y=int(time[0])
            m=int(time[1])
            d=int(time[2])
            h=int(time[3])
            min_time=int(time[4])
            s=int(time[5])
        
        return self.t.load_template('forms/dateform.phtml', yes_time=self.yes_time, form=self.name, y=y, m=m, d=d, h=h, min=min_time, s=s)

    #def 
                         
