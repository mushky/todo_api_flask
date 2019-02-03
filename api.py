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
	todo.insert({'text': input_json['text'], 'complete': input_json['complete']})
	return "Success"

# Get Todo by Id
@app.route('/api/v1/resources/todos/<id>', methods=['GET'])
def get_todo_by_id(id):
	todos = mongo.db.todos
	todo = todos.find_one({'_id':bson.ObjectId(oid=str(id))})

	sanitized = json.loads(json_util.dumps(todo))
	return jsonify(sanitized)

@app.route("/api/v1/resources/todos/<id>", methods=['DELETE'])
def remove_todo(id):
	todos = mongo.db.todos
	try:
		delete_todo = todos.delete_one({'_id':bson.ObjectId(oid=str(id))})

		if delete_todo.deleted_count > 0:
			# Prepare the response
			return "", 204
		else:
			# Resource not found
			return "", 404
	except:
		# Error while trying to delete the resource
		# Add message for debugging purpose
		return "", 500

@app.route('/api/v1/resources/todos/<id>', methods=['PUT'])
def update_todo(id):
	input_json = request.get_json(force=True)

	todos = mongo.db.todos
	todo = todos.update_one({'_id':bson.ObjectId(oid=str(id))}, {'$set': {'text': input_json['text']}})

	return 'updated'

@app.route('/api/v1/resources/todos/complete', methods=['GET'])
def complete_todo():
	the_id = request.args.get('id')

	print the_id

	todos = mongo.db.todos
	todo = todos.find_one({'_id':bson.ObjectId(oid=str(the_id))})
	if todo['complete'] == False:
		todos.update_one({'_id':bson.ObjectId(oid=str(the_id))},{'$set': {'complete': True }})
	else:
		todos.update_one({'_id':bson.ObjectId(oid=str(the_id))},{'$set': {'complete': False}})

	return 'complete'



app.run()