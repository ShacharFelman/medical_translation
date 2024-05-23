import unittest
from app import app

class EngineTestCase(unittest.TestCase):
    
    def setUp(self) -> None:
        self.app = app.test_client()
        self.app.testing = True

    
    def tearDown(self) -> None:
        return super().tearDown()
    
    
    # def test_translate(self):
    #     input_text = "hello"
    #
    #     response = self.app.post('/text', json={
    #         'referenceToken':"DUMMY",
    #         'source':"heb",
    #         'dest':"eng",
    #         'textInput':"שלום שמי הוא שמע ישראל"
    #     })
    #
    #     self.assertEqual(response.status_code, 200)



        
      

if __name__ == "__main__":
    unittest.main()