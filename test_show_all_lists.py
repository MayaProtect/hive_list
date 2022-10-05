import unittest
from pymongo import MongoClient
import show_all_lists
import flask_unittest
#from flask_app import create_app 
import flask
import json
from flask_cors import CORS, cross_origin
import os
from unittest.mock import MagicMock, patch

class TestGetHives(flask_unittest.ClientTestCase):
    app = create_app()
 
    # def __init__(self, methodName: str = ...) -> None:
    #     super().__init__(methodName)
    #     self.__db = 'mayaprotect'
    #     self.__collection = 'hives'
    #     self.__host = 'localhost'
    #     self.__port = '27017'
    #     self.__clientmongo = MongoClient('mongodb://' + self.__host + ':' + self.__port)
    
    
    
    @patch('test_show_all_lists.page_query', return_value = ["mocke"])   
    def test_get_result_page_with_client(self, client):
        
        rv = client.get('/hives')
        self.assertInResponse(rv,["mocke"])
        
if __name__ == "__main__":
    unittest.main()        
    