#!/usr/bin/python3

import sys
import pymysql.cursors

class SqlClass:
    
    error_connection=""
    connection={}
    
    def dummy_connect(self, connection, name_connection="default"):
        pass
    
    def connect_to_db(self, connection, name_connection="default"):
    
        try:
        
            self.connection[name_connection] = pymysql.connect(connection['host'],
                user=connection['user'],
                password=connection['password'],
                db=connection['db'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
            
            
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
    
    def close(self, name_connection="default"):
        
        self.connection[name_connection].close()
        
        pass
    
    