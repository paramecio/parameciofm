#!/usr/bin/python3

from math import ceil, floor
from paramecio.citoplasma.urls import add_get_parameters
from paramecio.citoplasma.i18n import I18n

class Pages: 

    css_class='link_pages'

    @staticmethod
    def show( begin_page, total_elements, num_elements, link ,initial_num_pages=20, variable='begin_page', label='', func_jscript=''):
        
        pages='';

        if begin_page>total_elements:
            begin_page=0

        # Calculamos el total de todas las páginas

        total_page=ceil(total_elements/num_elements)
        
        # Calculamos en que página nos encontramos

        actual_page=ceil(begin_page/num_elements)

        # Calculamos el total de intervalos

        total_interval=ceil(total_page/initial_num_pages)

        # Calculamos el intervalo en el que estamos

        actual_interval=floor(actual_page/initial_num_pages)

        # Calculamos el elemento de inicio del intervalo

        initial_page=ceil(actual_interval*initial_num_pages*num_elements)

        last_page=ceil(actual_interval*initial_num_pages*num_elements)+ceil(initial_num_pages*num_elements)

        if last_page>total_elements:
            last_page=total_elements

        if initial_page>0:
            initial_link=add_get_parameters(link, **{variable: '0'});
            middle_link=add_get_parameters(link, **{variable: str((initial_page-num_elements)) } );
            pages += "<a class=\""+Pages.css_class+"\" href=\""+initial_link+"\" onclick=\"func_jscript\">1</a> <a class=\""+Pages.css_class+"\" href=\""+middle_link+"\">&lt;&lt;</a> "

        arr_pages={}

        #for(x=initial_page;x<last_page;x+=num_elements)
        for x in range(initial_page, last_page, num_elements):
            
            middle_link=add_get_parameters(link, **{variable: str(x)} )

            num_page=ceil(x/num_elements)+1;
            arr_pages[x]="<a class=\""+Pages.css_class+"\" href=\""+middle_link+"\" onclick=\"func_jscript\">"+str(num_page)+"</a> "
            arr_pages[begin_page]='<span class="selected_page">'+str(num_page)+'</span> ';
            pages += arr_pages[x]

        
        if last_page<total_elements:

            middle_link=add_get_parameters(link, **{variable: str(x+num_elements)} );
            last_link=add_get_parameters(link, **{variable: str( ( ( total_page*num_elements ) - num_elements) ) } )

            pages += "<a class=\""+Pages.css_class+"\" href=\""+middle_link+"\" onclick=\"func_jscript\">&gt;&gt;</a> <a class=\"link_pages\" href=\""+last_link+"\" onclick=\"func_jscript\">"+I18n.lang('common', 'last', 'Last')+"</a>"

        
        return pages


