#!/usr/bin/env python3

import sys
import pymysql.cursors
pymysql.install_as_MySQLdb
import sqlalchemy.pool as pool
import traceback

mypool=None

class SqlClass:
    
    def __init__(self, connection):
    
        self.max_overflow=-1
        self.pool_size=15
        self.error_connection=""
        # Data of connection
        self.connection=connection
        # Sql connection
        self.conn=None
        self.connected=False
        self.pool_recycle=3600
        
    def connect(self):
        
        global mypool
      
        if self.conn==None:
            try:
                def getconn():
                    return pymysql.connect(self.connection['host'],
                        user=self.connection['user'],
                        passwd=self.connection['password'],
                        db=self.connection['db'],
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
				
                if mypool==None:
                    
                    mypool=pool.QueuePool(getconn, max_overflow=self.max_overflow, pool_size=self.pool_size, recycle=self.pool_recycle, use_threadlocal=False)

                self.conn=mypool.connect()

                self.conn.ping(True)
                
                """
                while not self.conn.open:
                    self.conn=SqlClass.mypool.connect()
                """
                
                self.connected=True

            except:
                e = sys.exc_info()[0]
                v = sys.exc_info()[1]

                self.error_connection="Error in connection: %s %s" % (e, v)

                self.conn.close()

                raise NameError(self.error_connection)
  
    
    #Make def query more simple if not debugging.
    
    def query(self, sql_query, arguments=[], name_connection="default"):
        
        self.connect()
        
        #if fetch_type=="ASSOC":
            #fetch_type=MySQLdb.cursors.DictCursor
        
        #with self.conn.cursor(MySQLdb.cursors.DictCursor) as cursor:
        cursor=self.conn.cursor(pymysql.cursors.DictCursor)
        
        try:
            
            cursor.execute(sql_query, arguments)
            self.conn.commit()
            
            return cursor
            
        
        except:
            e = sys.exc_info()[0]
            v = sys.exc_info()[1]
            
            if hasattr(cursor, '_last_executed'):
               sql_query=cursor._last_executed 
            #, traceback.format_exc()
            self.error_connection="Error in query ||%s||Values: %s" % (sql_query, str(arguments))
        
            #return False
            raise NameError(self.error_connection)
    
    #Fetcho row return dictionary if is defined in query.
    
    #def fetch(self, cursor):
        
        #return cursor.fetchone()
    
    def __del__(self):
        
        if self.conn:
        
            self.conn.close()
    
    def close(self, name_connection="default"):
        
        if self.conn:
        
            self.conn.close()
            self.conn=None
        
        pass
    
    
