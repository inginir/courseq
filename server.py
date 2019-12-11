from flask import Flask, jsonify, abort
import json

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

@app.route('/', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route('/courses', methods=['GET'])
def get_courses():
    with open('courses.json') as courses_json_file:
        data = json.load(courses_json_file)
        return jsonify(data)

if __name__ == '__main__':
    app.run()