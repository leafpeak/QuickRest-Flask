from flask import Flask
from flask import jsonify, abort, make_response, request

from todos import tasks

app = Flask(__name__)

@app.route('/todos', methods=['GET'])
def get_todos():
  '''
  curl -i http://127.0.0.1:5000/todos
  '''
  return jsonify({'todos': tasks})

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
  '''
  curl -i http://127.0.0.1:5000/todos/<id>
  '''
  todo = filter(lambda t: t['id'] == todo_id, tasks)
  if len(todo) == 0:
    abort(404)

  return jsonify(todo[0])

@app.route('/todos', methods=['POST'])
def post_todos():
  '''
  curl -i -H "Content-Type: application/json" -X POST -d '{"task":"do this"}' http://localhost:5000/todos
  '''
  if not request.json or not 'task' in request.json:
    abort(400)

  todo = {
    'id': tasks[-1]['id'] + 1,
    'task': request.json['task'],
    'complete': False
  }
  tasks.append(todo)

  return jsonify({'todo': todo}), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def put_todo(todo_id):
  '''
  curl -i -H "Content-Type: application/json" -X PUT -d '{"task":"do this"}' http://localhost:5000/todos/<id>
  '''
  todo = filter(lambda t: t['id'] == todo_id, tasks)
  if len(todo) == 0:
    abort(400)
  if not request.json:
    abort(400)
  if 'task' in request.json and type(request.json['task']) != unicode:
    abort(400)
  if 'complete' in request.json and type(request.json['complete']) != bool:
    abort(400)

  todo[0]['task'] = request.json.get('task')
  todo[0]['complete'] = request.json.get('complete')

  return jsonify({'todo': todo[0]})

@app.route('/todos/<int:todo_id>', methods=['PATCH'])
def patch_todo(todo_id):
  '''
  curl -i -H "Content-Type: application/json" -X PATCH -d '{"task":"do this"}' http://localhost:5000/todos/<id>
  '''
  todo = filter(lambda t: t['id'] == todo_id, tasks)
  if len(todo) == 0:
    abort(400)
  if not request.json:
    abort(400)
  if 'task' in request.json and type(request.json['task']) != unicode:
    abort(400)
  if 'complete' in request.json and type(request.json['complete']) != bool:
    abort(400)

  if 'task' in request.json:
    todo[0]['task'] = request.json.get('task')
  if 'complete' in request.json:
    todo[0]['complete'] = request.json.get('complete')

  return jsonify({'todo': todo[0]})

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  '''
  curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/todos/<id>
  '''
  todo = filter(lambda t: t['id'] == todo_id, tasks)
  if len(todo) == 0:
    abort(404)

  tasks.remove(todo[0])

  return jsonify({'deleted': True})

@app.errorhandler(404)
def not_found(error):

  return make_response(jsonify( { 'error': 'Not found' } ), 404)


if __name__ == '__main__':
  app.run(debug=True)
