#!/usr/bin/python3

def show_links(switch, arr_links):

    final_links=[]

    for link in arr_links:
        
        if link[0]==switch:
            
            final_links.append(link[1])
            
            break
        else:
            
            final_links.append('<a href="'+link[2]+'">'+link[1]+'</a>')

    return final_links