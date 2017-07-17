#!/usr/bin/env python3

from paramecio.cromosoma.coreforms import BaseForm
from paramecio.citoplasma.mtemplates import env_theme, PTemplate

env=env_theme(__file__)

t=PTemplate(env)

class FileForm(BaseForm):

    def __init__(self, name, value, path):
        
        super().__init__(name, value)
        
        self.t=t
        self.enctype=True

    def form(self):
        
        return self.t.load_template('forms/fileform.phtml', form=self)
