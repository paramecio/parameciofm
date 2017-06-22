#/usr/bin/env python3

from paramecio.citoplasma.urls import add_get_parameters

class HierarchyLinks:

    def __init__(arr_links, t=None):

        self.arr_links=arr_links
        
        self.arr_indexes={}
    
    def update_links(self, link_father, link_son, text):
    
        self.arr_links[link_father][link_son]=text
    
    
    def calculate_indexes():
    
        #oreach(self.arr_links as $father_link => $arr_child_links)
        for father_link, arr_child_links in self.arr_links.items():
            
            #foreach($arr_child_links as $link => $text)
            for link, text in self.arr_child_links.items():
                
                self.arr_indexes[link]=father_link

    
    def result(last_link, arr_result=[], yes_last_link=0):
    
        self.calculate_indexes()
        
        if last_link in self.arr_indexes:
            
            father=self.arr_indexes[last_link]
            
            arr_last_link[0]=self.no_link
            
            arr_last_link[1]=self.yes_link
            
            yes_link_func=arr_last_link[yes_last_link]
            
            if father!='':
                
                arr_result.append(self.yes_link_func(last_link, self.arr_links[father][last_link]))
                
                yes_last_link=1
                
                arr_result=self.result(father, arr_result, yes_last_link)
                
                return arr_result
            
            else:
                
                arr_result.append(self.yes_link_func(last_link, self.arr_links[father][last_link]))
                
                return arr_result
        
        return arr_result
    
    
    def show(link, separator='&gt;&gt;', class_link=''):
    
        arr_result=self.result(link)
        
        arr_result=array_reverse(arr_result)
        
        return ' '+separator+' '.join(arr_result)
    
    def yes_link(link, text):
    
        return '<a href="'+link+'">'+text+'</a>'

    
    def no_link(link, text):
    
        return text

class HierarchyModelLinks:
    
    def __init__(self, model, first_element_title, field_name, field_parent, base_url):
        
        self.model=model
        self.field_parent=field_parent
        self.field_name=field_name
        self.base_url=base_url
        self.arr_parent={}
        self.arr_son=[]
        self.first_element_title=first_element_title
    
    def prepare(self):
        
        with self.model.set_conditions('', []).select([self.model.name_field_id, self.field_name, self.field_parent]) as cur:
            for arr_model in cur:
                if self.field_parent not in self.arr_parent:
                    self.arr_parent[arr_model[self.model.name_field_id]]=[]
                
                self.arr_parent[arr_model[self.model.name_field_id]]=[arr_model[self.field_name], arr_model[self.field_parent]]
        
    def parents(self,  son_id, url_func):
        
        if son_id not in self.arr_parent or son_id==0:
            return 
        
        self.arr_son.insert(0, url_func(son_id, self.arr_parent[son_id][0]))
        
        self.parents(self.arr_parent[son_id][1], self.url)
        
    
    def no_url(self, son_id, title):
        return title
        
    def url(self, son_id, title):
        
        args={}
        
        args[self.field_parent]=str(son_id)
        
        return '<a href="%s">%s</a>' % (add_get_parameters(self.base_url, **args), title)
    
    def show(self, son_id, separator=' &gt;&gt; '):
        
        try:
            son_id=int(son_id)
        except:
            son_id=0
        
        self.prepare()
        
        self.parents(son_id, self.no_url)
        
        self.arr_son.insert(0, self.url(0, self.first_element_title))
        
        return separator.join(self.arr_son)
            
        
                
            
            
        
