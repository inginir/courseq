import functools
from flask import Flask, jsonify, abort, request
import json
# import requests

from generator import tst_fn, generate, Course

tst_fn()

app = Flask(__name__)

def course_mapper(course):
    return Course(
        code= course['code'], 
        name = course['name'], 
        credits= course['credits'], 
        season_availability=course['seasons'], 
        prereqs=course['prereqs'], 
        coreqs=course['coreqs']
    )

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

@app.route('/generate-sequence', methods=['POST'])
def generate_sequence():
    data = request.get_json()
    def courses_transformer(acc, course):
        return {**acc, course['code']:course_mapper(course)}

    courses_transformed = functools.reduce(courses_transformer, data['courses'], dict())

    # sequence = generate(courses_transformed)
    sequence_refilled = generate(courses_transformed, data['locked_courses'])
    response = jsonify(sequence_refilled.to_jsonable())
    return response

@app.route('/shuffle-sequence', methods=['POST'])
def shuffle_sequence():
    data = request.get_json()
    sequence_refilled = generate(data['terms'], data['locked_courses'])
    response = jsonify(sequence_refilled.to_jsonable())
    return response


if __name__ == '__main__':
    app.run()