from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mydb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mongotask'

mongo = PyMongo(app)
CORS(app)

@app.route("/")
def hello():
    return "Hello World!"
    
@app.route('/items', methods=['GET'])
def get_all_items():
    items = mongo.db.items 

    output = []
    for item in items.find():
        output.append({'_id': str(item['_id']), 'name' : item['name'], 'description' : item['description']})

    return jsonify({'result' : output})

@app.route('/items/<name>', methods=['GET'])
def get_item(name):
    items = mongo.db.items

    item = items.find_one({'name' : name})

    if item:
        output = {'name' : item['name'], 'description' : item['description']}
    else:
        output = 'No results found'

    return jsonify({'result' : output})

@app.route('/items', methods=['POST'])
def add_item():
    items = mongo.db.items

    name = request.json['name']
    description = request.json['description']

    item_id = items.insert({'name' : name, 'description' : description})
    item = items.find_one({'_id' : item_id})

    output = {'name' : item['name'], 'description' : item['description']}

    return jsonify({'result' : output})

@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    items = mongo.db.items

    name = request.json['name']
    description = request.json['description']

    items.update_one({'_id':ObjectId(id)}, {"$set": {"name": name, "description": description}})
    item = items.find_one({'_id' : ObjectId(id)})
    output = {'name' : item['name'], 'description' : item['description']}

    return jsonify({'result' : output})

@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    items = mongo.db.items
    returned = items.delete_one({'_id':ObjectId(id)})
    if returned.deleted_count == 1:
        output = {'message': 'deleted'}
    else:
        output = {'message': 'not deleted'}
    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)