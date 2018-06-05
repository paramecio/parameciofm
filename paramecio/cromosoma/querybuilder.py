#!/usr/bin/env python3

from collections import OrderedDict
import sys

def query(model, str_query, args=[], connection_id='default'):
        
    model.connect_to_db()
    
    return model.sqlclass.query(str_query, args, connection_id)

# Insert method, for insert a row in database.using a dictionary
# External agent define if the update is in code or from external source, how a form.

def insert(model, dict_values, external_agent=True):
    
    model.clean_fields()
    
    # Connect to db

    model.post=dict_values

    #model.connect_to_db()
    
    query_error=False
    last_sql=''
    
    #model.fields[model.name_field_id].required=False
    
    if model.name_field_id in dict_values:
        del dict_values[model.name_field_id]
    
    try:
        
        fields, values, update_values=model.check_all_fields(dict_values, external_agent)
        
    except: 

        query_error=(model.sqlclass.error_connection+' '+sys.exc_info()[0], '')
        #cursor.close()
        return (query_error, False)

    
    c=len(values)
    
    arr_str=['%s' for x in range(c)]
    
    sql="insert into `"+model.name+"` (`"+"`, `".join(fields)+"`) VALUES ("+", ".join(arr_str)+")"
    
    last_sql=sql
    
    cursor=model.query(sql, values, model.connection_id)
    
    if cursor.rowcount>0:
        
        model.last_id=cursor.lastrowid
        
        cursor.close()
        
        # Delete cache for this table.
        
        return (False, True)
    else:
        query_error=('Cannot insert the new row', last_sql)
        
        
        return (query_error, False)

class QueryBuilderException(Exception):
    pass
    
def select(model, conditions=['', []], arr_select=[], raw_query=False):
    
    model.clean_fields()

    final_fields=[]
        
    extra_fields=[]
    
    #model.query_error=''
    query_error=False
    last_query=''
    
    #First table selecction
    
    tables_to_select=['`'+model.name+'`']
    
    keys=list(model.fields.keys())
    
    if len(arr_select)==0:
        arr_select=keys
    
    # Array intersect for obtain the valid fields
    
    fields =  list(set(keys) & set(arr_select))
    
    #Creating the fields
    arr_repeat_field={}
    
    new_fields=OrderedDict()
    for field in fields:
        
        #Check if foreignkeyfield
        
        if type(model.fields[field]).__name__=="ForeignKeyField" and raw_query==False:
            
            if model.fields[field].table_name in arr_repeat_field:
                arr_repeat_field[model.fields[field].table_name]+=1
                
            else:
                arr_repeat_field[model.fields[field].table_name]=0
            
            table_name=model.fields[field].table_name+'` as `'+model.fields[field].table_name+str(arr_repeat_field[model.fields[field].table_name])
            
            final_table_name=model.fields[field].table_name+str(arr_repeat_field[model.fields[field].table_name])
            
            # The name with its alias of this related table model
            
            tables_to_select.append('`'+table_name+'`')
            
            # Add field from related table
            # as "+table_name+"_"+model.fields[field].named_field
            extra_fields.append("`"+final_table_name+"`.`"+model.fields[field].named_field+"` as "+field)
            
            # Add a condition to sql query for join the two tables.
            
            conditions[0]+=" AND `"+final_table_name+"`.`"+model.fields[field].identifier_field+"`=`"+model.name+"`.`"+field+"`"
            
            # Add extra fields from related table from select_fields ForeignKeyField class member
            
            select_fields=model.fields[field].select_fields
            
            for extra_field in select_fields:
                
                model.fields[field+'_'+extra_field]=model.fields[field].related_model.fields[extra_field]
                model.fields_to_clean.append(field+'_'+extra_field)
                
                # Check if extra_field is ForeignKeyField, if yes, call this function recursively.
            
                extra_fields.append("`"+final_table_name+"`.`"+extra_field+"` as `"+field+"_"+extra_field+"`")
        else:
            # Add normal field to sql query
            
            final_fields.append("`"+model.name+"`.`"+field+"`")
    
    #if len(new_fields)>0:
        #model.fields.update(new_fields)
    
    extra_sql_field=""
    
    if len(extra_fields)>0:
        
        extra_sql_field=", "+", ".join(extra_fields)
        
    if len(final_fields)==0:
        query_error=("Error: without fields to search", '')
        #return (query_error, False)
        raise QueryBuilderException("Error: without fields to search")
    
    sql= ("select "+" "+model.distinct+", ".join(final_fields)+extra_sql_field+" from "+", ".join(tables_to_select)+' '+conditions[0]).strip()
    
    last_query=sql
    
    cursor=model.query(sql, conditions[1], model.connection_id)
    
    if cursor==False:
        #query_error=(model.sqlclass.error_connection, last_query)
        #cursor.close()
        #return (query_error, False)
        raise QueryBuilderException(model.sqlclass.error_connection+last_query)
    else:
        return cursor

def select_to_array(model, conditions=['', []], fields_selected=[], raw_query=0):
        
    if len(fields_selected)==0:
        fields_selected=model.fields.keys()
    
    if (model.name_field_id not in fields_selected):
        fields_selected.append(model.name_field_id)
        def del_row_id(row):
            
            try:
            
                index_id=row.index(model.name_field_id)
                
                del row[index_id]
                
            except:
                
                pass
    else:
        def del_row_id(row):
            pass
    
    results=[] #OrderedDict()
    
    with select(model, conditions, fields_selected, raw_query) as cursor:        
        for row in cursor:
            
            if model.show_formatted and row:
                for k, col in row.items():
                    if model.fields[k].show_formatted_value:
                        row[k]=self.fields[k].show_formatted(col)
            
            results.append(row)
        
        del_row_id(results)
    
    return results

def select_to_dict(model, conditions=['', []], fields_selected=[], raw_query=0, integer_dict=False):    
    
    if not integer_dict:
        def conv_int(i):
            return str(i)
    else:
        def conv_int(i):
            return i        
    
    if len(fields_selected)==0:
        fields_selected=model.fields.keys()
    
    if (model.name_field_id not in fields_selected):
        fields_selected.append(model.name_field_id)
        def del_row_id(row):
            
            try:
            
                index_id=row.index(model.name_field_id)
                
                del row[index_id]
                
            except:
                
                pass
    else:
        def del_row_id(row):
            pass
    
    results=OrderedDict()
    
    with select(model, conditions, fields_selected, raw_query) as cursor:        
        for row in cursor:

            if model.show_formatted and row:
                for k, col in row.items():
                    row[k]=model.fields[k].show_formatted(col)

            results[conv_int(row[model.name_field_id])]=row
        
        del_row_id(results)
    
    return results

def select_a_row_where(model, conditions=['', []], fields_selected=[], raw_query=0, begin=0):
    
    limit="limit "+str(begin)+", 1"
    
    with select(model, conditions, fields_selected, raw_query) as cursor:
    
        row=cursor.fetchone()
        
        if row==None:
            row=False
        else:
            if model.show_formatted:
                for k, col in row.items():
                    row[k]=model.fields[k].show_formatted(col)
    
    return row

def select_a_row(model, id, fields_selected=[], raw_query=0):
    
    conditions=['WHERE `'+model.name+'`.`'+model.name_field_id+'`=%s', [id]]
    
    with select(model, conditions, fields_selected, raw_query) as cursor:
    
        row=cursor.fetchone()
        
        if row==None:
            row=False
        else:
            if model.show_formatted:
                for k, col in row.items():
                    row[k]=model.fields[k].show_formatted(col)
    return row


# A method por count num rows affected for sql conditions

def select_count(model, conditions=['', []], field_to_count='id', raw_query=True):
    
    
    #First table selecction
    
    tables_to_select=['`'+model.name+'`']
    
    fields=list(model.fields.keys())
    
    #Creating the fields
    
    for field in fields:
        
        #Check if foreignkeyfield
        
        if type(model.fields[field]).__name__=="ForeignKeyField"  and raw_query==False:
            
            table_name=model.fields[field].table_name
            
            tables_to_select.append('`'+table_name+'`')
            
            # Add a condition to sql query for join the two tables.
            
            conditions[0]+=" AND `"+table_name+"`.`"+model.fields[field].identifier_field+"`=`"+model.name+"`.`"+field+"`"
            
    sql= "select count(`"+field_to_count+"`) from "+", ".join(tables_to_select)+' '+conditions[0]
    
    count=0
    
    with model.query(sql, conditions[1], model.connection_id) as cursor:
        count=list(cursor.fetchone().values())[0]
        
        if model.yes_reset_conditions:
            model.reset_conditions()
    
    return count

