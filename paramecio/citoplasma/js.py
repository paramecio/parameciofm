from paramecio.citoplasma.sessions import get_session
from paramecio.citoplasma.i18n import I18n
from settings import config

def make_js_url(file_path, module):

    #/mediajs/<module>/<lang>/<filename:path>
    s=get_session()
    
    lang=I18n.get_default_lang()

    return config.base_url+'mediajs/%s/%s/%s' % (module, lang, file_path)
