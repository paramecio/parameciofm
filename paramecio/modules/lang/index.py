from paramecio.citoplasma.i18n import I18n
from bottle import get,response,request, redirect
from paramecio.citoplasma.sessions import get_session
import re

@get('/change_lang/<lang>')
def index(lang):
    
    if lang in I18n.dict_i18n:
        
        s=get_session()
        
        s['lang']=lang
        
        redirect_url=request.headers.get('Referer')
        
        if redirect_url!=None:
            
            #if not re.match('.*\/change_lang\/.*', request.path):
        
            redirect(redirect_url)
        
    return ""