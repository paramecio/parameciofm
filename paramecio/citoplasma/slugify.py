#!/usr/bin/python

#A very simple version of strtr of php.

def strtr(str_in, pat_str, rep_str):
	
	ret_str=''
	
	arr_dict={}
	
	if(len(pat_str)!=len(rep_str)):
		raise NameError('Ups, pat_str len != rep_str len')
	
	#Create dictionary
	
	for (i, l) in enumerate(pat_str):
		arr_dict[l]=rep_str[i]
	
	#Make a for to the str_in and substr.
	
	for le in str_in:
		
		if le in arr_dict:
			
			ret_str+=arr_dict[le]
			
		else:
			ret_str+=le
	
	return (ret_str)

def slugify(str_in, respect_upper=False, replace_space='-', replace_dot=False, replace_barr=False):
	
	str_out=''
	
	from_str='àáâãäåæçèéêëìíîïðòóôõöøùúûýþÿŕñÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÐÒÓÔÕÖØÙÚÛÝỲŸÞŔÑ¿?!¡()"|#*%,;+&$ºª<>`çÇ{}@~=^:´[]\''
	to_str=  'aaaaaaaceeeeiiiidoooooouuuybyrnAAAAAACEEEEIIIIDOOOOOOUUUYYYBRN----------------------------------'
	
	if replace_dot==True:
		
		from_str+='.'
		from_to+='-'

	
	if replace_barr==True:
	
		from_str+="/"
		to_str+="-"
	
	str_out=str_in.strip()
	
	str_out=strtr(str_out, from_str, to_str)

	str_out=str_out.replace(" ", replace_space)
	
	if respect_upper==False:
		str_out=str_out.lower()
	
	return str_out
	
