from settings import config
from paramecio.cromosoma.webmodel import WebModel
from paramecio.cromosoma import corefields
import unittest


# Create TestWebModelMethods

class ExampleModel(WebModel):
    
    def create_fields(self):

        # I can change other fields here, how the name.

        self.register(corefields.CharField('title'))
        self.register(corefields.CharField('content'))

model=ExampleModel()

class TestWebModelMethods(unittest.TestCase):
    
    def test_test_table(self):
        
        sql=model.create_table()
        
        print('Creating table')
        
        self.assertTrue(WebModel.query(WebModel, sql))
        
        post={'title': 'Example title', 'content': 'New content'}
        
        model.set_valid_fields()
        
        print('Insert row')
        
        self.assertTrue(model.insert(post))
        
        print('Check new id')
        
        self.assertEqual(model.insert_id(), 1)
        
        post={'title': 'Example title Updated', 'content': 'New content Updated'}
        
        model.conditions=['WHERE id=%s', [1]]  
        
        print('Update row')
        
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
        
        self.assertEqual(model.select_to_array(['title', 'content']), {1: {'title': 'Example title Updated', 'content': 'New content Updated'}})
        
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
    
    def test_update_table(self):
    
        print('Check modifications in table')
    
        sql=model.create_table()
        
        self.assertTrue(WebModel.query(WebModel, sql))
        
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
    
if __name__ == '__main__':
    unittest.main()
    