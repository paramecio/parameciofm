from settings import config
from paramecio.cromosoma.webmodel import WebModel
from paramecio.cromosoma import corefields
import unittest
# Create TestWebModelMethods

class ExampleModel(WebModel):
    
    def __init__(self, connection):

        super().__init__(connection)

        # I can change other fields here, how the name.

        self.register(corefields.CharField('title'))
        self.register(corefields.CharField('content'))
        
class ForeignKeyExampleModel(WebModel):
    
    def __init__(self, connection):

        super().__init__(connection)

        # I can change other fields here, how the name.
        
        self.register(corefields.CharField('name'))
        self.register(corefields.ForeignKeyField('example_id', ExampleModel(connection), size=11, required=False, identifier_field='id', named_field="id", select_fields=[]))
        
        
class ExampleModel2(WebModel):
    
    def __init__(self, connection):

        super().__init__(connection)

        # I can change other fields here, how the name.

        self.register(corefields.CharField('title'))
        self.register(corefields.CharField('content'))

class TestWebModelMethods(unittest.TestCase):
    
    def test_test_table(self):
        
        connection=WebModel.connection()
        model=ExampleModel(connection)

        
        sql=model.create_table()
        
        print('Creating table')
        
        self.assertTrue(model.query(sql))

        
        post={'title': 'Example title', 'content': 'New content'}
        
        model.set_valid_fields()
        
        print('Insert row')
        
        self.assertTrue(model.insert(post))
        
        print('Check new id')
        
        self.assertEqual(model.insert_id(), 1)
        
        post={'title': 'Example title Updated', 'content': 'New content Updated'}
        
        model.conditions=['WHERE id=%s', [1]]  
        
        print('Updating row')
        
        self.assertTrue(model.update(post))
        
        model.yes_reset_conditions=False
        
        model.conditions=['WHERE id=%s', [1]]
        
        print('Count rows')
        
        self.assertEqual(model.select_count(), 1)
        
        print('Select a row')
        
        self.assertEqual(model.select_a_row(1, ['title']), {'title': 'Example title Updated'})
        
        print('Select a row with different conditions to search id')
        
        self.assertEqual(model.select_a_row_where(['title']), {'title': 'Example title Updated'})
        
        print('Select and save in an array')
        
        self.assertEqual(model.select_to_array(['title', 'content']), [{'id': 1, 'title': 'Example title Updated', 'content': 'New content Updated'}])
        
        model.yes_reset_conditions=True
        
        model.reset_conditions()
        
        print('Reset conditions')
        
        self.assertEqual(model.conditions, ['WHERE 1=1', []])
    
        print('Simple base select')
    
        cur=model.select()
        
        row=model.fetch(cur)
        
        self.assertEqual(row, {'id': 1, 'title': 'Example title Updated', 'content': 'New content Updated'})
        
        print('Check element exists')
        
        self.assertTrue(model.element_exists(1))
        
        model.conditions=['WHERE id=%s', [2]]
        
        print('Check delete row')
        
        self.assertFalse(model.delete())
        
        self.assertTrue(model.delete())
        
        print('Check delete table')
        
        self.assertTrue(model.drop())
        
        connection.close()
        
    
    def test_update_table(self):
    
        connection=WebModel.connection()
        model=ExampleModel(connection)

    
        print('Check modifications in table')
    
        sql=model.create_table()
        
        self.assertTrue(model.query(sql))
        
        fields_to_modify=[]
        fields_to_add_index=[] 
        fields_to_add_constraint=[]
        fields_to_add_unique=[]
        fields_to_delete_index=[]
        fields_to_delete_unique=[]
        fields_to_delete_constraint=[]
        fields_to_delete=[]
        
        model.register(corefields.CharField('description'))
        
        model.update_table(['description'], fields_to_modify, fields_to_add_index, fields_to_add_constraint, fields_to_add_unique, fields_to_delete_index, fields_to_delete_unique, fields_to_delete_constraint, fields_to_delete)
        
        model.register(corefields.IntegerField('description'))
        
        model.update_table([], ['description'], ['description'], [], ['description'], fields_to_delete_index, fields_to_delete_unique, fields_to_delete_constraint, fields_to_delete)
        
        model.update_table([], fields_to_modify, fields_to_add_index, fields_to_add_constraint, fields_to_add_unique, ['description'], ['description'], fields_to_delete_constraint, ['description'])
        
        self.assertTrue(model.drop())
        
        connection.close()
    
    def test_conditions(self):
        
        print('Test conditions')
        
        connection=WebModel.connection()
        model=ExampleModel(connection)
        
        sql=model.create_table()
        
        self.assertTrue(model.query(sql))
        
        cur=model.set_conditions('where id=%s', [4]).select()
        
        self.assertTrue(cur)
        
        cur.close()
        
        self.assertTrue(model.drop())
        
        connection.close()

    def test_functions(self):
        
        print('Test functions')
        
        connection=WebModel.connection()
        model=ExampleModel(connection)
        
        sql=model.create_table()
        
        self.assertTrue(model.query(sql))
        
        cur=model.set_conditions('where id=%s', [4]).select()
        
        self.assertTrue(cur)
        
        cur.close()
        
        self.assertTrue(model.drop())
        
        connection.close()
    
    def test_zcheck_1_foreignkeys(self):
        
        connection=WebModel.connection()
        model=ExampleModel(connection)
        foreignkey=ForeignKeyExampleModel(connection)
        
        print('Checking ForeignKeys models...')
        
        sql=model.create_table()
        sqlf=foreignkey.create_table()
        
        print('Creating foreignkey table...')
        
        self.assertTrue(model.query(sql))
        self.assertTrue(foreignkey.query(sqlf))
        
        for k_field, index in WebModel.arr_sql_index['foreignkeyexamplemodel'].items():
            print("---Added index to "+k_field)
            foreignkey.query(index)
                
        for k_set, index_set in WebModel.arr_sql_set_index['foreignkeyexamplemodel'].items():
            
            if index_set!="":
                connection.query(index_set)
                print("---Added constraint to "+k_set)
        
        model.create_forms()
        
        self.assertTrue(model.insert({'title': 'Foreign title', 'content': 'Foreign content'}))
        
        my_id=model.insert_id()
        
        foreignkey.create_forms()
        
        self.assertTrue(foreignkey.insert({'example_id': my_id, 'name': 'Relationship'}))
        
        print('Checking insert...')
        
        foreignkey.set_conditions('where example_id=%s', [my_id])
        
        self.assertEqual(foreignkey.select_count(), 1)
        
        model.set_conditions('where id=%s', [my_id])
        
        self.assertTrue(model.delete())
        
        foreignkey.set_conditions('where example_id=%s', [my_id])
        
        print('Checking automatic delete...')
        
        self.assertEqual(foreignkey.select_count(), 0)
        
        print('Dropping foreignkey table...')
        
        self.assertTrue(foreignkey.drop())
        self.assertTrue(model.drop())       
        
        pass
        
    def test_zcheck_connections(self):
        
        print('Check connection of models...')
        
        connection=WebModel.connection()
        model=ExampleModel(connection)
        
        model2=ExampleModel2(connection)
        
        sql=model.create_table()
        sql2=model2.create_table()
        #print(sql)
        
        self.assertTrue(model.query(sql))
        self.assertTrue(model2.query(sql2))
        
        self.assertTrue(model.drop())
        self.assertTrue(model2.drop())
        
        connection.close()
        
        pass
        
    def test_check_filter_list_str(self):
        
        print('Check string list filtering')

        connection=WebModel.connection()
        model=ExampleModel(connection)

        str_filter=model.check_in_list_str('title', ['joan', 'piter', 'luiz"'])
        
        self.assertEqual(str_filter, '("joan", "piter", "luiz&quot;")')
        
        connection.close()
    
if __name__ == '__main__':
    unittest.main()
    
