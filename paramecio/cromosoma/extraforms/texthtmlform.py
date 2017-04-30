
from paramecio.cromosoma.coreforms import BaseForm
from paramecio.citoplasma.mtemplates import env_theme, PTemplate

env=env_theme(__file__)

t=PTemplate(env)

class TextHTMLForm(BaseForm):
    
    def __init__(self, name, value, t_add=None):
        
        super().__init__(name, value)
        
        self.t=t_add
        
        if t_add==None:
            self.t=t
        
    def form(self):
        
        return self.t.load_template('forms/texthtmlform.phtml', form=self)
