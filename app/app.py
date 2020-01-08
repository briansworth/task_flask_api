from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

tasks = [
  {
    'id': 1,
    'title': u'Make a thing',
    'description': u'Make the thing, or A thing',
    'done': False
  },
  {
    'id': 2,
    'title': u'Lean the thing',
    'description': u'Learn to do the thing!',
    'done': False
  }
]

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

# LIST TASKS
@app.route('/api/v1/tasks', methods=['GET'])
def get_tasks():
  return jsonify({'tasks': tasks})

# GET TASK
@app.route('/api/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
  task = [task for task in tasks if task['id'] == task_id]
  if len(task) == 0:
    abort(404)
  return jsonify({'task': task[0]})

# CREATE TASK
@app.route('/api/v1/tasks', methods=['POST'])
def create_task():
  if not request.json:
    abort(400)
  if not request.json['title']:
    abort(400, description="No task title defined")
  task = {
    'id': tasks[-1]['id'] + 1,
    'title': request.json['title'],
    'description': request.json.get('description', ""),
    'done': False
  }
  tasks.append(task)
  return jsonify({'task': task}), 201

# UPDATE TASK
@app.route('/api/v1/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
  task = [task for task in tasks if task['id'] == task_id]
  if len(task) == 0:
    abort(404)
  if not request.json:
    abort(400)
  if 'done' in request.json and type(request.json['done']) is not bool:
    abort(400, description="Property 'done' is not of type 'bool'")
  task[0]['title'] = request.json.get('title', task[0]['title'])
  task[0]['description'] = request.json.get('description', task[0]['description'])
  task[0]['done'] = request.json.get('done', task[0]['done'])
  return jsonify({'task': task[0]})

# DELETE TASK
@app.route('/api/v1/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
  task = [task for task in tasks if task['id'] == task_id]
  if len(task) == 0:
    abort(404)
  tasks.remove(task[0])
  return jsonify({})
