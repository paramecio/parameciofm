#/usr/bin/python3

class HierarchyLinks:

    def __init__(arr_links):

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

