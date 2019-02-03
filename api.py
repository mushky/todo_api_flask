import flask 
from flask import request, jsonify
from flask_pymongo import PyMongo
import bson
from bson import json_util, ObjectId
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['MONGO_DBNAME'] = 'TodoDB'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Todo'

mongo = PyMongo(app, uri = "mongodb://localhost:27017/TodoDB")

# Get all todos
@app.route('/api/v1/resources/new', methods=['POST'])
def new():
	input_json = request.get_json(force=True)

	todo = mongo.db.todos
	todo.insert({'id': input_json['id'], 'text': input_json['text'], 'complete': input_json['complete']})
	return "Success"

# Post Todo
@app.route('/api/v1/resources/todos/all', methods=['GET'])
def get_all_todos():
	todos = mongo.db.todos
	output = []
	for todo in todos.find():
		output.append({'id' : todo['id'], 'text' : todo['text'], 'complete' : todo['complete']})
	return jsonify({'result' : output})

# Get Todo by Id
@app.route('/api/v1/resources/todos/<id>', methods=['GET'])
def get_todo_by_id(id):
	todos = mongo.db.todos
	todo = todos.find_one({'_id':bson.ObjectId(oid=str(id))})
	print todo

	sanitized = json.loads(json_util.dumps(todo))
	return jsonify(sanitized)

# Update ID
def update_todo():
	id = request.values.get("_id")
	todo = todos.find({"_id":ObjectId(id)})
		

app.run()