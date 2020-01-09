from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, reqparse, fields, marshal

app = Flask(__name__, static_url_path="")
api = Api(app)

tasks = [
  {
    'id': 1,
    'title': u'Make a thing',
    'description': u'Make the thing, or A thing',
    'done': False
  },
  {
    'id': 2,
    'title': u'Learn the thing',
    'description': u'Learn to do the thing!',
    'done': False
  }
]

task_fields = {
  'title': fields.String,
  'description': fields.String,
  'done': fields.Boolean,
  'uri': fields.Url('task')
  #'id': fields.Integer
}

class TaskListAPI(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()
    
    self.reqparse.add_argument(
      'title',
      type=str,
      required=True,
      help='Task property Title not provided',
      location='json'
    )
    self.reqparse.add_argument(
      'description',
      type=str,
      default='',
      location='json'
    )

    super(TaskListAPI, self).__init__()

  def get(self):
    return {'tasks': [marshal(task, task_fields) for task in tasks]}

  def post(self):
    args = self.reqparse.parse_args()
    task = {
      'id': tasks[-1]['id'] + 1 if len(tasks) > 0 else 1,
      'title': args['title'],
      'description': args['description'],
      'done': False
    }
    tasks.append(task)
    return {'task': [marshal(task, task_fields)]}, 201

class TaskAPI(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()

    self.reqparse.add_argument('title', type=str, location='json')
    self.reqparse.add_argument('description', type=str, location='json')
    self.reqparse.add_argument('done', type=bool, location='json')
    self.reqparse.add_argument('id', type=int, location='json')

    super(TaskAPI, self).__init__()

  def get(self, id):
    task = [task for task in tasks if task['id'] == id]
    if len(task) == 0:
      abort(404)

    return {'task': [marshal(task[0], task_fields)][0]}

api.add_resource(TaskListAPI, '/api/v1/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/api/v1/tasks/<int:id>', endpoint='task')

if __name__ == '__main__':
  app.run(debug=True)
