import pymongo
import flask
import json
import bson
from uuid import UUID, uuid4
from flask_cors import CORS, cross_origin
from os import environ as env


app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

# pour apres le function get_collection



def get_collection():
    my_client = pymongo.MongoClient('mongodb://' + env.get('MONGO_HOST') + ':' + env.get('MONGO_PORT') + '/')
    # my_client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = my_client['mayaprotect']
    hives = db['hives']
    return hives


@app.route('/hives', methods=['GET'])    
@cross_origin() 
# 打印所有蜂巢信息
def page_query():
    args = flask.request.args
    page_size = int(args.get("limit")) if args.get("limit") is not None else 25
    page_on = int(args.get("page")) if args.get("page") is not None else 1
    skip = page_size * (page_on - 1)
    coll = get_collection()
    
   
    dict_filtre = {}
    if args.get("station_id") is not None:
        dict_filtre['station_uuid'] = bson.Binary.from_uuid(UUID(args.get('station_id')))
    
    if args.get("owner_id") is not None:
        dict_filtre['owner.uuid'] = bson.Binary.from_uuid(UUID(args.get('owner_id')))
    
    
    page_record = coll.find(dict_filtre).limit(page_size).skip(skip)
    hives_to_return = []
    for hive in page_record:
        hive_to_add_to_result = {
            "id": str(UUID(bytes=hive['uuid'])),  
            "station_id": str(UUID(bytes=hive['station_uuid']))
        }
        hives_to_return.append(hive_to_add_to_result)
    
   # return flask.Response(json.dumps(hives_to_return), mimetype='application/json')
    return flask.Response(json.dumps(hives_to_return), mimetype='application/json')

    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)