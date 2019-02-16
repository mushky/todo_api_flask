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
@app.route('/api/v1/resources/todos/all', methods=['GET'])
def get_all_todos():
	todos = mongo.db.todos
	output = []
	for todo in todos.find():
		output.append({'text' : todo['text'], 'complete' : todo['complete']})
	return jsonify({'result' : output})

# Post Todo
@app.route('/api/v1/resources/new', methods=['POST'])
def new():
	input_json = request.get_json(force=True)

	todo = mongo.db.todos

	todo_id = todo.insert({'text': input_json['text'], 'complete': input_json['complete']})
	new_todo = todo.find_one({"_id" : todo_id})
	
	output = {'text': new_todo['text'], 'complete': new_todo['complete']}

	return jsonify({'result': output})

# Get Todo by Id
@app.route('/api/v1/resources/todos/<id>', methods=['GET'])
def get_todo_by_id(id):
	todos = mongo.db.todos
	todo = todos.find_one({'_id':bson.ObjectId(oid=str(id))})

	sanitized = json.loads(json_util.dumps(todo))
	return jsonify(sanitized)

# Delete Todo by id
@app.route("/api/v1/resources/todos/<id>", methods=['DELETE'])
def remove_todo(id):
	todos = mongo.db.todos
	try:
		delete_todo = todos.delete_one({'_id':bson.ObjectId(oid=str(id))})

		if delete_todo.deleted_count > 0:
			return "", 204
		else:
			return "", 404
	except:
		# Add message for debugging purpose
		return "", 500

# Update Todo by id
@app.route('/api/v1/resources/todos/<id>', methods=['PUT'])
def update_todo(id):
	input_json = request.get_json(force=True)

	todos = mongo.db.todos
	todo = todos.update_one({'_id':bson.ObjectId(oid=str(id))}, {'$set': {'text': input_json['text']}})

	return 'updated'

# Toggle Complete boolean of todo
@app.route('/api/v1/resources/todos/complete', methods=['GET'])
def complete_todo():
	id = request.args.get('id')

	todos = mongo.db.todos
	todo = todos.find_one({'_id':bson.ObjectId(oid=str(id))})
	todoStatus = todos.update_one({'_id':bson.ObjectId(oid=str(id))},{'$set': {'complete': True }}) if todo['complete'] == False else todos.update_one({'_id':bson.ObjectId(oid=str(id))},{'$set': {'complete': False}})

	return 'complete called'


if __name__ == "__main__":
	app.run()
