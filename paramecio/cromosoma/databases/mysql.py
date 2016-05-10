#!/usr/bin/python3

import sys
import pymysql
pymysql.install_as_MySQLdb()

class SqlClass:
    
    def __init__(self):
    
        self.error_connection=""
        self.connection={}
        self.connected=False
        self.connection_method=self.connect_to_db_sql
    
    def dummy_connect(self, connection, name_connection="default"):
        pass
    
    def connect_to_db(self, connection, name_connection="default"):
        
        self.connection_method(connection, name_connection)
        
        self.connection_method=self.dummy_connect
        
    def connect_to_db_sql(self, connection, name_connection="default"):
        
        try:
        
            self.connection[name_connection] = pymysql.connect(connection['host'],
                user=connection['user'],
                passwd=connection['password'],
                db=connection['db'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
            
            self.connected=True
            
        except:
            e = sys.exc_info()[0]
            v = sys.exc_info()[1]
            
            self.error_connection="Error in connection: %s %s" % (e, v)
            
            #return False
            raise NameError(self.error_connection)
    
    #Make def query more simple if not debugging.
    
    def query(self, sql_query, arguments=[], name_connection="default"):
        
        #if fetch_type=="ASSOC":
            #fetch_type=pymysql.cursors.DictCursor
        
        with self.connection[name_connection].cursor(pymysql.cursors.DictCursor) as cursor:
            
            try:
                
                cursor.execute(sql_query, arguments)
                self.connection[name_connection].commit()
                
                return cursor
            
            except:
                e = sys.exc_info()[0]
                v = sys.exc_info()[1]
                
                if hasattr(cursor, '_last_executed'):
                   sql_query=cursor._last_executed 
                
                self.error_connection="Error in query ||"+sql_query+"||: %s %s" % (e, v)
            
                #return False
                raise NameError(self.error_connection)
    
    #Fetcho row return dictionary if is defined in query.
    
    #def fetch(self, cursor):
        
        #return cursor.fetchone()
    """
    def __del__(self):
        
        for key in self.connection:
        
            self.close(self.connection)
    """
    
    def close(self, name_connection="default"):
        
        if self.connection[name_connection]:
        
            self.connection[name_connection].close()
            self.connection[name_connection]=False
        
        pass
    
    
