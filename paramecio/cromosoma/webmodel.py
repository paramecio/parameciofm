#!/usr/bin/env python3

import sys
import re
import uuid
from importlib import import_module, reload
from collections import OrderedDict
from paramecio.cromosoma.databases.mysqldb import SqlClass
from paramecio.cromosoma.coreforms import BaseForm, HiddenForm
import copy
import traceback

class PhangoField:
    
    def __init__(self, name, size=255, required=False):
        
        # The name of the field in database table
        
        self.name=name
        
        # The label for the Field
        
        self.label=name.replace('_', ' ').title()
        
        # If field is required, self.required is True
        
        self.required=required
        
        # The size of field in database
        
        self.size=size
        
        # Protected, if this value != False, cannot use it in insert or update.
    
        self.protected=False
        
        # $quote_open is used if you need a more flexible sql sentence, 
        # @warning USE THIS FUNCTION IF YOU KNOW WHAT YOU ARE DOING
        
        self.quot_open='\''
        
        # $quote_close is used if you need a more flexible sql sentence, 
        # @warning USE THIS PROPERTY IF YOU KNOW WHAT YOU ARE DOING
        
        self.quot_close='\''
        
        # Variable where the basic text error is saved
    
        self.error=None
        
        self.txt_error=""
        
        # Themodel where this component or field live
    
        self.model=None
        
        # Property used for set this field how indexed in the database table.

        self.indexed=False
        
        # Property used for set this field how unique value in the database table.

        self.unique=False
        
        # Simple property for make more easy identify foreignkeyfields.
        
        self.foreignkey=False
        
        # Property that define the default value for this field
        
        self.default_value=""
     
        # Property that define if this field is in an update operation or insert operation
        
        self.update=False
        
        # Property used for check if this value cannot change if is in blank and is filled
        
        self.check_blank=False
        
        # Define the form, when is created forms with create_forms you can change the properties of this class
        
        self.name_form=BaseForm
        
        # Property that define if make escape in show_formatted.  This property control the html transformation  of <>" characters in html entities.If false, convert.
        
        self.escape=False
        
        # File related: if the field have a file related, delete the file
        
        self.file_related=False
        
        # Extra parameters for the form
        
        self.extra_parameters=[]
        
        # Template manager for the form if needed
        
        self.t=None
     
    # This method is used for describe the new field in a sql language format.
    

    def get_type_sql(self):

        return 'VARCHAR('+str(self.size)+') NOT NULL DEFAULT "'+self.default_value+'"'
    
    def show_formatted(self, value):
        
        return value
    
    # This method for check the value
    

    def check(self, value):
        
        self.error=False
        self.txt_error=''
        
        value=str(value)
        
        if self.escape==False:        
            value=value.replace('<', '&lt;')
            
            value=value.replace('>', '&gt;')
            
            value=value.replace('"', '&quot;')
        
        #value=WebModel.escape_sql(value)
        
        if value=="":
            self.txt_error="The field is empty"
            self.error=True
            
        
        return value
    
    def set_relationships(self):
        pass
    
    def create_form(self):
        #self.name, self.default_value, 
        
        final_parameters=copy.copy(self.extra_parameters)
        
        final_parameters.insert(0, self.name)
        final_parameters.insert(1, self.default_value)
        form=self.name_form(*final_parameters)
        form.default_value=self.default_value
        form.required=self.required
        form.label=self.label
        form.field=self
        return form
    
    def change_form(self, new_form, parameters):
        
        self.name_form=new_form
        
        self.extra_parameters=parameters
        
    def post_register(self):
        pass

class PrimaryKeyField(PhangoField):
    
    def __init__(self, name, size=11, required=False):
        super(PrimaryKeyField, self).__init__(name, size, required)
        self.protected=True
        self.name_form=HiddenForm
        self.required=True
    
    def check(self, value):
        
        self.error=None
        self.txt_error=''
        
        if value=='':
            value='0'
        
        try:
        
            value=str(int(value))
        
        except:
            
            value=0
        
        if value==0:
            self.txt_error="The value is zero"
            self.error=True
            
        
        return value
    
    def get_type_sql(self):

        return 'INT NOT NULL PRIMARY KEY AUTO_INCREMENT'

# The most important class for the framework
#
# Webmodel is a class for create objects that represent models. This models are a mirage of SQL tables. You can create fields, add indexes, foreign keys, and more.
#
#        
        

class WebModel:
    
    __slots__=('sqlclass', 'fields', 'forms')
    
    #Globals class variables for internal tasks
    
    arr_sql_index={}
    arr_sql_set_index={}
    arr_sql_unique={}
    arr_sql_set_unique={}
    last_query=""
    connection_pool=[]
    first_primary_key=PrimaryKeyField('id')
    
    #A dictionary for add models here
    
    model=OrderedDict()
    
    connections={'default': {'host': 'localhost', 'user': 'user', 'password': '', 'db': 'default', 'charset': 'utf8', 'set_connection': False} }
        
    connection_id="default"
    
    webmodel=True
    
    global_cached=False
    
    #sqlclass=SqlClass()
    
    #make_connection=sqlclass.connect_to_db
    
    @staticmethod
    def connection():
        
        return SqlClass(WebModel.connections['default'])
    
    # Init the class
    
    def __init__(self, sqlclass, name_field_id="id"):
        
        self.cached=self.global_cached
        
        self.cached_runquery=self.global_cached
        
        self.type_cache='file'
        
        #The name of the table
        
        self.name=type(self).__name__.lower()
        
        self.label=self.name
        
        self.label_general=self.name
        
        self.name_field_id=name_field_id
        
        #Fields of the table, inserte with register method
        
        self.fields=OrderedDict()
        
        #The tables related with foreignkeyfield to this table
        
        self.related=[]
        
        #A dictionary where forms of this model are saved
        
        self.forms=OrderedDict()
        
        self.cache_method=''
        
        # A dictionary with the errors in fields.
        
        self.fields_errors={}
        
        self.errors={}
        
        self.num_errors=0
        
        self.query_error=""
        
        self.values_query=[]
        
        self.conditions=["WHERE 1=1", []]
        
        self.order_by="ORDER BY `"+self.name+"`.`id` ASC"
        
        self.limit=""
        
        self.related_models_deleted=[]
        
        self.required_save={}
        
        #Create id field
        
        primary_key=WebModel.first_primary_key
        
        primary_key.name=self.name_field_id
        
        self.register(primary_key)
        
        #self.register(PrimaryKeyField(self.name_field_id))
        
        #self.model[name]=self
        
        self.yes_reset_conditions=True
        
        #self.create_fields()
        
        self.updated=False
        
        self.valid_fields=[]
        
        self.last_id=0
        
        self.distinct=''
        
        # A simple dictionary where post values are saved for use of fields classes
        
        self.post={}
        
        # A simple dictionary that save the fields that have files related. If i delete the row in database i need delete the files related
        
        self.files_delete={}
        
        self.sqlclass=sqlclass
        
        self.fields_to_clean=[]
        
        self.create_fields()

    # A method where create the new fields of this model
    
    def create_fields(self):
        
        #print([i for i in dir(self.__class__) if i[:1] != '_'])
        #print(dir(self))
        
        pass
    
    # A method for register the fields
    
    def register(self, field_model, required=False):
        
        #self.fields_required[field_model]=field_model.required
        
        self.fields[field_model.name]=field_model
        
        self.fields[field_model.name].model=self
        
        self.fields[field_model.name].required=required
        
        self.fields[field_model.name].post_register()
        
        #self.files_delete[field_model.name]=field_model.file_related
    
    # A method for create the id field.
    
    def create_id_field(self, field_name="id"):
        pass
    
    # A method for connect to database
    
    def connect_to_db(self):
        
        #if WebModel.make_connection(self.connections[self.connection_id])==False:
            #raise NameError(sqlclass.error_connection)
        
        #self.connection_pool.append(True)
        
        
        #if self.sqlclass.connect_to_db(self.connections[self.connection_id])==False:
        #    raise NameError(sqlclass.error_connection)
        
        #WebModel.make_connection=sqlclass.dummy_connect
        pass
    
    def dummy_connect(self, connection):
        return True
    
    # Static method for make queries
    
    def query(self, str_query, args=[], connection_id='default'):
        
        self.connect_to_db()
        return self.sqlclass.query(str_query, args, connection_id)
    
    # Method for clean fields
    
    def clean_fields(self):
        for field in self.fields_to_clean:
            del self.fields[field]
    
    # Insert method, for insert a row in database.using a dictionary
    # External agent define if the update is in code or from external source, how a form.
    
    def insert(self, dict_values, external_agent=True):
        
        self.clean_fields()
        
        # Connect to db

        self.post=dict_values

        self.connect_to_db()
        
        self.query_error=''
        
        self.fields[self.name_field_id].required=False
        
        try:
            
            fields, values, update_values=self.check_all_fields(dict_values, external_agent)
            
        except: 
            self.query_error='Cannot insert the new row'

            return False
        
        c=len(values)
        
        arr_str=['%s' for x in range(c)]
        
        sql="insert into `"+self.name+"` (`"+"`, `".join(fields)+"`) VALUES ("+", ".join(arr_str)+")"
        
        cursor=self.sqlclass.query(sql, values, self.connection_id)
        
        if cursor.rowcount>0:
            
            self.last_id=cursor.lastrowid
            
            cursor.close()
            
            return True
        else:
            self.query_error='Cannot insert the new row'
            
            cursor.close()
            
            return False
    
    # Update method. For update one or many rows.
    
    def update(self, dict_values, external_agent=True):
        
        self.clean_fields()
        
        self.post=dict_values
        
        # Connect to db
        
        self.fields[self.name_field_id].required=False
        
        if self.name_field_id in dict_values:
            del dict_values[self.name_field_id]

        self.connect_to_db()
        
        self.query_error=''
        
        #try:
        self.updated=True
        
        try:
            
            fields, values, update_values=self.check_all_fields(dict_values, external_agent, True, 'update')
            
        except: 
            
            #self.query_error+="\n"+traceback.format_exc()
            
            return False
        
        sql="update `"+self.name+"` SET "+", ".join(update_values)+" "+self.conditions[0]
        
        cursor=self.sqlclass.query(sql, values+self.conditions[1], self.connection_id)
        
        if self.yes_reset_conditions:
            self.reset_conditions()
        
        cursor.close()
        
        return True
        
        """
        if cursor.rowcount>0:
            
            if self.yes_reset_conditions:
                self.reset_conditions()
            
            return True
        
        else:
            
            self.query_error='Cannot update the row'
            
            return False
        """
        """
        except:
            
            #self.query_error=sqlclass.error_connection
            e = sys.exc_info()[0]
            v = sys.exc_info()[1]
            
            self.error_connection="Error in query: %s %s" % (e, v)
            
            return False
        """

    def reset_conditions(self):

        self.conditions=["WHERE 1=1", []]
        
    
    # A method for select fields from a table in db. Support for foreignkeys.
    #Type assoc can be assoc for return dictionaries
    
    def select(self, arr_select=[], raw_query=False):
        
        self.clean_fields()
        
        # Connect to db
        
        self.connect_to_db()
        
        conditions=self.conditions
        
        final_fields=[]
        
        extra_fields=[]
        
        self.query_error=''
        
        #First table selecction
        
        tables_to_select=['`'+self.name+'`']
        
        keys=list(self.fields.keys())
        
        if len(arr_select)==0:
            arr_select=keys
        
        # Array intersect for obtain the valid fields
        
        fields =  list(set(keys) & set(arr_select))
        
        #Creating the fields
        arr_repeat_field={}
        
        new_fields=OrderedDict()
        for field in fields:
            
            #Check if foreignkeyfield
            
            if type(self.fields[field]).__name__=="ForeignKeyField" and raw_query==False:
                
                if self.fields[field].table_name in arr_repeat_field:
                    arr_repeat_field[self.fields[field].table_name]+=1
                    
                else:
                    arr_repeat_field[self.fields[field].table_name]=0
                
                table_name=self.fields[field].table_name+'` as `'+self.fields[field].table_name+str(arr_repeat_field[self.fields[field].table_name])
                
                final_table_name=self.fields[field].table_name+str(arr_repeat_field[self.fields[field].table_name])
                
                # The name with its alias of this related table model
                
                tables_to_select.append('`'+table_name+'`')
                
                # Add field from related table
                # as "+table_name+"_"+self.fields[field].named_field
                extra_fields.append("`"+final_table_name+"`.`"+self.fields[field].named_field+"` as "+field)
                
                # Add a condition to sql query for join the two tables.
                
                conditions[0]+=" AND `"+final_table_name+"`.`"+self.fields[field].identifier_field+"`=`"+self.name+"`.`"+field+"`"
                
                # Add extra fields from related table from select_fields ForeignKeyField class member
                
                for extra_field in self.fields[field].select_fields:
                    
                    self.fields[field+'_'+extra_field]=self.fields[field].related_model.fields[extra_field]
                    self.fields_to_clean.append(field+'_'+extra_field)
                    
                    # Check if extra_field is ForeignKeyField, if yes, call this function recursively.
                
                    extra_fields.append("`"+final_table_name+"`.`"+extra_field+"` as `"+field+"_"+extra_field+"`")
            else:
                # Add normal field to sql query
                
                final_fields.append("`"+self.name+"`.`"+field+"`")
        
        #if len(new_fields)>0:
            #self.fields.update(new_fields)
        
        extra_sql_field=""
        
        if len(extra_fields)>0:
            
            extra_sql_field=", "+", ".join(extra_fields)
            
        if len(final_fields)==0:
            self.query_error="Error: without fields to search"
            return False
        
        sql= ("select "+" "+self.distinct+", ".join(final_fields)+extra_sql_field+" from "+", ".join(tables_to_select)+' '+conditions[0]+' '+self.order_by+' '+self.limit).strip()
        
        self.last_query=sql
        
        if self.yes_reset_conditions:
            self.reset_conditions()
        
        cursor=self.sqlclass.query(sql, conditions[1], self.connection_id)
        
        if cursor==False:
            self.query_error=self.sqlclass.error_connection
            cursor.close()
            return False
        else:
            return cursor
        
    # Show results in a dictionary
    
    def fetch(self, cursor):
        
        return cursor.fetchone()
    
    def insert_id(self):
        
        return self.last_id
    
    def element_exists(self, id):
        
        self.conditions=['WHERE `'+self.name_field_id+'`=%s', [id]]
        
        count=self.select_count(self.name_field_id)
        
        if self.yes_reset_conditions:
            self.reset_conditions()
        
        if count>0:
            return True

        return False
    
    def select_a_field(self, field):
        pass
    
    def select_a_row(self, id, fields_selected=[], raw_query=0):
        
        self.conditions=['WHERE `'+self.name+'`.`'+self.name_field_id+'`=%s', [id]]
        
        self.limit="limit 1"
        
        with self.select(fields_selected, raw_query) as cursor:        
            self.reset_conditions()
            
            row=cursor.fetchone()
            
            if row==None:
                row=False

        return row
    
    def select_a_row_where(self, fields_selected=[], raw_query=0, begin=0):
        
        self.limit="limit "+str(begin)+", 1"
        
        with self.select(fields_selected, raw_query) as cursor:
        
            row=cursor.fetchone()
            
            if row==None:
                row=False
        
        return row
    
    
    def select_to_array(self, fields_selected=[], raw_query=0):
        
        if len(fields_selected)==0:
            fields_selected=self.fields.keys()
        
        if (self.name_field_id not in fields_selected):
            fields_selected.append(self.name_field_id)
            def del_row_id(row):
                
                try:
                
                    index_id=row.index(self.name_field_id)
                    
                    del row[index_id]
                    
                except:
                    
                    pass
        else:
            def del_row_id(row):
                pass
        
        results=[] #OrderedDict()
        
        with self.select(fields_selected, raw_query) as cursor:        
            for row in cursor:
                
                results.append(row)
            
            del_row_id(results)
        
        return results
        
    
    # A method por count num rows affected for sql conditions
    
    def select_count(self, field_to_count='id', raw_query=True):
        
        # Connect to db
        
        self.connect_to_db()
        
        conditions=self.conditions
        
        #First table selecction
        
        tables_to_select=['`'+self.name+'`']
        
        fields=list(self.fields.keys())
        
        #Creating the fields
        
        for field in fields:
            
            #Check if foreignkeyfield
            
            if type(self.fields[field]).__name__=="ForeignKeyField"  and raw_query==False:
                
                table_name=self.fields[field].table_name
                
                tables_to_select.append('`'+table_name+'`')
                
                # Add a condition to sql query for join the two tables.
                
                conditions[0]+=" AND `"+table_name+"`.`"+self.fields[field].identifier_field+"`=`"+self.name+"`.`"+field+"`"
                
        sql= "select count(`"+field_to_count+"`) from "+", ".join(tables_to_select)+' '+conditions[0]
        
        count=0
        
        with self.sqlclass.query(sql, conditions[1], self.connection_id) as cursor:
            count=list(cursor.fetchone().values())[0]
            
            if self.yes_reset_conditions:
                self.reset_conditions()
        
        return count
        
        #+' ORDER BY '+self.order_by+' '+self.limit).strip()
    
    # A method for delete rows using sql conditions
    
    def delete(self):
        
        self.connect_to_db()
        
        #Need delete rows from other related tables save in self.related_models_deleted
        
        sql="delete from `"+self.name+"` "+self.conditions[0]
        
        result=self.sqlclass.query(sql, self.conditions[1], self.connection_id)
        
        if self.yes_reset_conditions:
            self.reset_conditions()
        
        if result.rowcount>0:
        
            result.close()
            return True
        else:
            
            result.close()
            return False
    
    def set_conditions(self, sql_text, values:list) -> None:
        
        self.conditions=[sql_text, values]
        
        return self
    
    def set_order(self, order:list, position:list) -> None:
        
        order=[]
        
        for o in enumerate(order):
        
            order.append('order by '+order[o]+' '+position[o])
    
        self.order=", ".join(order)
    
    def set_limit(self, limit: tuple) -> None:
        
        sql_limit=str(limit[0])
        
        if len(limit)>1:
            sql_limit+=', '+str(limit[1])
        
        self.limit='limit '+sql_limit
    
    # Method for create sql tables
    
    def create_table(self):
        
        #self.connect_to_db()
        
        self.arr_sql_index[self.name]={}
        self.arr_sql_set_index[self.name]={}
        self.arr_sql_unique[self.name]={}
        self.arr_sql_set_unique[self.name]={}
        
        #foreach($this->components as $field => $data)
        table_fields=[]
        
        #Create id field
        #Not neccesary
        #table_fields.append('`'+self.name_field_id+"` INT NOT NULL PRIMARY KEY AUTO_INCREMENT")
        
        for field, data in self.fields.items():
        
            table_fields.append('`'+field+'` '+data.get_type_sql())
            
            #Check if indexed
            
            if self.fields[field].indexed==True:
            
                self.arr_sql_index[self.name][field]='CREATE INDEX `index_'+self.name+'_'+field+'` ON '+self.name+'(`'+field+'`);'
                self.arr_sql_set_index[self.name][field]=""
            
            
            #Check if unique
            
            if self.fields[field].unique==True:
            
                self.arr_sql_unique[self.name][field]='ALTER TABLE `'+self.name+'` ADD UNIQUE (`'+field+'`)'
                self.arr_sql_set_unique[self.name][field]=""
                
            if type(self.fields[field]).__name__=="ForeignKeyField":
                
                self.arr_sql_index[self.name][field]='CREATE INDEX `index_'+self.name+'_'+field+'` ON '+self.name+'(`'+field+'`);'
                
                table_related=self.fields[field].table_name
                
                id_table_related=self.fields[field].table_id            
                
                self.arr_sql_set_index[self.name][field]='ALTER TABLE `'+self.name+'` ADD CONSTRAINT `'+field+'_'+self.name+'IDX` FOREIGN KEY ( `'+field+'` ) REFERENCES `'+table_related+'` (`'+id_table_related+'`) ON DELETE CASCADE ON UPDATE CASCADE;'
        
        return "create table `"+self.name+"` (\n"+",\n".join(table_fields)+"\n) DEFAULT CHARSET=utf8;";
            
    def update_table(self, fields_to_add, fields_to_modify, fields_to_add_index, fields_to_add_constraint, fields_to_add_unique, fields_to_delete_index, fields_to_delete_unique, fields_to_delete_constraint, fields_to_delete):
        
        # First delete fields
        
        for field in fields_to_delete_index:
            
            print("---Deleting index from "+field+" in "+self.name)
            
            self.query('DROP INDEX `index_'+self.name+'_'+field+'` ON '+self.name, [], self.connection_id)
        
        for field in fields_to_delete_unique:
            
            print("---Deleting unique from "+field+" in "+self.name)
            
            self.query('DROP INDEX `'+field+'` ON '+self.name, [], self.connection_id)
        
        for field in fields_to_delete_constraint:
            
            print("---Deleting foreignkey from "+field+" in "+self.name)
            
            self.query('ALTER TABLE `'+self.name+'` DROP FOREIGN KEY '+field+'_'+self.name+'IDX', [], self.connection_id)
        
        for field in fields_to_delete:
            
            print("---Deleting "+field+" from "+self.name)
            
            self.query('ALTER TABLE `'+self.name+'` DROP `'+field+'`', [], self.connection_id)
            #Deleting indexes and constraints.
        
        #Obtain new fields
        
        for field in fields_to_modify:
            print("---Updating "+field+" in "+self.name)
            self.query('ALTER TABLE `'+self.name+'` MODIFY `'+field+'` '+self.fields[field].get_type_sql(), [], self.connection_id)
        
        for field in fields_to_add:
            print("---Adding "+field+" in "+self.name)
            self.query('ALTER TABLE `'+self.name+'` ADD `'+field+'` '+self.fields[field].get_type_sql(), [], self.connection_id)
            
        for field in fields_to_add_index:
            print("---Adding index to "+field+" in "+self.name)
            self.query('CREATE INDEX `index_'+self.name+'_'+field+'` ON '+self.name+' (`'+field+'`);', [], self.connection_id)
            
        for field in fields_to_add_constraint:
            
            print("---Adding foreign key to "+field+" in "+self.name)
            
            table_related=self.fields[field].table_name
                
            id_table_related=self.fields[field].table_id
            
            self.query('ALTER TABLE `'+self.name+'` ADD CONSTRAINT `'+field+'_'+self.name+'IDX` FOREIGN KEY ( `'+field+'` ) REFERENCES `'+table_related+'` (`'+id_table_related+'`) ON DELETE CASCADE ON UPDATE CASCADE;', [], self.connection_id)
            
        for field in fields_to_add_unique:
            
            print("---Adding unique to "+field+" in "+self.name)
            
            self.query('ALTER TABLE `'+self.name+'` ADD UNIQUE (`'+field+'`)', [], self.connection_id)
            
        
        
    # Method for drop sql tables and related
    
    def drop(self):
        return self.query('DROP TABLE '+self.name, [], self.connection_id)
    
    #Return an array with all fields
    
    def all_fields():
        pass
    
    #Check of all fields in table.
    
    def check_all_fields(self, dict_values, external_agent, yes_update=False, errors_set="insert"):
        
        fields=[]
        values=[]
        update_values=[]
        self.errors[errors_set]=[]
        self.num_errors=0
        #A dictionary that define if update property is added
        
        updated_field={}
        updated_field['insert']=0
        updated_field['update']=1
        
        
        error=False
        
        if yes_update==True:
            f_update=lambda field, value: "`"+field+"`=%s"
        else:
            f_update=lambda field, value: ""
        
        # I can optimize this later
        
        for k, v in self.fields.items():
            
            #List where the errors are saved
            
            self.fields_errors[k]=[]
            
            if k in dict_values:
                
                # If fields is protected, but external_agent =0, then insert
                # If fields is not protected always insert if not error checking
                
                value=dict_values[k]
                
                # Cleaning the error
                
                self.fields[k].error=False
                
                if (self.fields[k].protected==None or self.fields[k].protected==False or external_agent==False):
                    
                    if k in self.valid_fields:
                        
                        self.fields[k].update=updated_field[errors_set]
                        
                        value=self.fields[k].check(value)
                        
                        if self.fields[k].check_blank==False or self.updated==False:
                            
                            # If error checking, value=False
                            
                            if self.fields[k].error==True and self.fields[k].required==True:
                                
                                #Error, need this fields.
                                self.num_errors+=1
                                
                                self.fields_errors[k].append("Error: "+v.label+" field required")
                                
                                error=True
                                
                            else:

                                fields.append(k)
                                
                                #final_value=self.fields[k].quot_open+value+self.fields[k].quot_close
                                #final_value=self.fields[k].quot_open+value+self.fields[k].quot_close
                                
                                values.append(value)
                                
                                update_values.append(f_update(k, value))
                    else:
                        self.num_errors+=1
                        
                        self.fields_errors[k].append("Error: "+self.fields[k].label+" is not in valid fields")
                        self.fields[k].error=True
                        self.fields[k].txt_error="Error: "+self.fields[k].label+" is not in valid fields"
                        error=True
                       
                else:
                    self.num_errors+=1
                    
                    self.fields_errors[k].append("Error: "+self.fields[k].label+" is protected field")
                    self.fields[k].error=True
                    self.fields[k].txt_error="Error: "+self.fields[k].label+" is protected field"
                    error=True
            
            elif v.required==True:
                
                self.num_errors+=1
                
                self.fields_errors[k].append("Error: "+v.label+" field required")
                error=True
        
        if len(fields)==0:
            
            self.num_errors+=1
            
            self.errors[errors_set].append("Error: no elements to insert in table")
            
            error=True
        
        if error==True:
            
            self.num_errors+=1
            
            self.errors[errors_set].append("Error: error checking the values of the table")
            
            return False
        
        return (fields, values, update_values)
    
    
    #Reset the require field in fields
    
    def reset_require(self):

        for k, v in self.fields.items():

            self.required_save[k]=self.fields[k].required
            self.fields[k].required=False
    
    
    #Reload the require field in fields
    
    def reload_require(self):
        
        for k,r in self.fields.items():
            self.fields[k].required=r

    #Choose all fields to updated
    
    def set_valid_fields(self, fields={}):
        
        if len(fields)==0:
            fields=self.fields.keys()
            
        self.valid_fields=fields
    
    #Create a form based in table.
    
    def create_forms(self, arr_fields=[]):
        
        self.forms=OrderedDict()
        
        if len(arr_fields)==0:
            arr_fields=list(self.fields.keys())
            
        if self.name_field_id in arr_fields:
            del arr_fields[arr_fields.index(self.name_field_id)]
        
        #for name_field, field in self.fields.items():
        for name_field in arr_fields:
            self.valid_fields.append(name_field)
            self.forms[name_field]=self.fields[name_field].create_form()

        return arr_fields
            
    def create_form_after(self, form_after, new_form):
        
        new_dict=OrderedDict()
        
        for name_form, form in self.forms.items():
            new_dict[name_form]=form
            if name_form==form_after:
                new_dict[new_form.name]=new_form
                
        self.forms=new_dict
    
    def show_errors(self):
        
        arr_error=[]
        error_txt=''
        
        for k_error in self.fields_errors.values():
            
            for error in k_error:
                arr_error.append(error)

        for type_error in self.errors.values():
            for error in type_error:
                arr_error.append(error)

        arr_error.append(self.query_error)
        
        error_txt="\n".join(arr_error)

        return error_txt
        
    def collect_errors(self):
        
        arr_error= {}
        error_txt=''
        
        for field_error, k_error in self.fields_errors.items():
            
            for error in k_error:
                arr_error[field_error]=error
        """
        for type_error in self.errors.values():
            for error in type_error:
                arr_error[field_error]=error
        """
        
        return arr_error
    
    def close(self):
        
        self.sqlclass.close()
        
        #connection_to_delete=[]
        
        #WebModel.make_connection=self.sqlclass.connect_to_db
        
        #for key in self.sqlclass.connection:
            #self.sqlclass.close(key)
            #connection_to_delete.append(key)
         
        #self.sqlclass.connection={} 
            
        #for key in connection_to_delete:
            #del sqlclass.connection[key]
    
    def escape_sql(value):
        
        value=str(value)
        
        return value.replace("'","\\'").strip()
    """
    def __del__(self):
        
        self.close()
    """
    
