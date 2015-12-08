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
        
        self.assertTrue(WebModel.query(WebModel, sql))
        
        post={'title': 'Example title', 'content': 'New content'}
        
        model.set_valid_fields()
        
        self.assertTrue(model.insert(post))
        
        self.assertEqual(model.insert_id(), 1)
        
        post={'title': 'Example title Updated', 'content': 'New content Updated'}
        
        model.conditions=['WHERE id=%s', [1]]  
        
        self.assertTrue(model.update(post))
        
        model.yes_reset_conditions=False
        
        model.conditions=['WHERE id=%s', [1]]
        
        self.assertEqual(model.select_count(), 1)
        
        self.assertEqual(model.select_a_row(1, ['title']), {'title': 'Example title Updated'})
        
        self.assertEqual(model.select_a_row_where(['title']), {'title': 'Example title Updated'})
        
        model.yes_reset_conditions=True
        
        model.reset_conditions()
        
        self.assertEqual(model.conditions, ['WHERE 1=1', []])
        
        cur=model.select()
        
        row=model.fetch(cur)
        
        self.assertEqual(row, {'id': 1, 'title': 'Example title Updated', 'content': 'New content Updated'})
        
        
        self.assertTrue(model.element_exists(1))
        
        self.assertTrue(model.drop())
    
if __name__ == '__main__':
    unittest.main()
    