import pymongo
import flask
from app.response_creator import ResponseCreator
import bson
import json
from uuid import UUID
from flask_cors import CORS, cross_origin


class GetHivesList:
    def __init__(self, params):
        self.params = params
        self.app = flask.Flask(__name__) 
        CORS(self.app)
        self.my_client = pymongo.MongoClient("mongodb://" + params['mongo_host'] + ":" + params['mongo_port'] + "/")
        self.db = self.my_client[params['mongo_db']]
        self.default_limit = params['default_limit']
        # Register routes
        # ???????????????????????????? rout ?? add_url_rule
        self.app.add_url_rule('/hives', 'get_hives', self.get_hives, methods=['GET'])
        # Set CORS
         # ????????????
        self.app.config['CORS_HEADERS'] = 'Content-Type'

    @cross_origin()
    def get_hives(self) -> flask.Response:
        """
        Get hives from DB and return them
        :return: Flask response
        """
        args = flask.request.args
        page_size = int(args.get("limit", self.params['default_limit']))
        page_on = int(args.get("page", 1))
        #??? page_on = int(args.get("page")) if args.get("page") is not None else 1
        skip = page_size * (page_on - 1)
        coll = self.__get_collection()
       
        dict_filtre = self.__make_filter(args)

        page_record = coll.find(dict_filtre).limit(page_size).skip(skip)
        total_record = coll.count_documents(dict_filtre)
        #???
        data_to_respond = ResponseCreator(page_record, total_record, page_on, page_size)

        return flask.Response(json.dumps(data_to_respond.create_response()), mimetype='application/json')

    def __get_collection(self) -> pymongo.collection.Collection:
        """
        :return: MongoDB collection
        """
        hives = self.db['hives']
        return hives

    def __make_filter(self, args) -> dict:
        """
        :param args: Flask request args
        :return: Filters for MongoDB
        """
        dict_filtre = {}
        if args.get("station_id") is not None:
            dict_filtre['station_uuid'] = bson.Binary.from_uuid(UUID(args.get('station_id')))
        if args.get("owner_id") is not None:
            dict_filtre['owner.uuid'] = bson.Binary.from_uuid(UUID(args.get('owner_id')))
        return dict_filtre

    def run(self) -> None:
        """
        Run Flask app
        """
        self.app.run(host='0.0.0.0', port=8080)
