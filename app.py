from flask import Flask
from flask import jsonify, make_response, request
from flask import Response
from flask_restful import Resource, Api, reqparse

import pandas as pd
import mongo_connect_query as mc
from flask import request
import logging
import os
import json
from bson import json_util, ObjectId



app = Flask(__name__)
api = Api(app)

DATABASE = 'test_main'
COLLECTION1 = 'Attempts'
COLLECTION2 = 'Assignments'
CLUSTER = "mongodb+srv://dev_user:Durham@cluster0.wu3em.mongodb.net/<dbname>?retryWrites=true&w=majority"
# URL = 'localhost:443'
HTTPS = False
# password is 'durham'

# BELOW FUNCTIONS ARE OUTDATED
"""
@app.route('/attempt', methods=['GET'])
def api_getattempt():
    attempt_id = request.headers.get('AttemptID')
    q = mc.Query(db.client)
    q.database = DATABASE
    q.collection = COLLECTION1
    data = q.getOneAttempt(attempt_id)
    if data is not None:
        data.pop('_id')
        return json.loads(json_util.dumps(data)), 200
    else:
        return "attempt not found", 404
@app.route('/attempt', methods=['PUT'])
def api_setattempt():
    attempt_data = request.json
    q = mc.Query(db.client)
    q.database = DATABASE
    q.collection = COLLECTION1
    response = q.insertOneAttempt(attempt_data)
    if response == 2:
        return "updated existing attempt", 200
    else:
        return "attempt set", 200
@app.route('/attempt', methods=['DELETE'])
def api_delattempt():
    attempt_id = request.headers.get('AttemptID')
    q = mc.Query(db.client)
    q.database = DATABASE
    q.collection = COLLECTION1
    response = q.deleteOneAttempt(attempt_id)
    if response == 0:
        return "attempt does not exist", 403
    else:
        return "attempt deleted", 200
"""

# GET A SINGLE ASSIGNMENT FROM DATABASE
@app.route('/assignment', methods=['GET'])
def api_getassignment():
    assignment_id = request.headers.get('AssignmentID')
    print(assignment_id)
    q = mc.Query(db.client)
    q.database = DATABASE
    q.collection = COLLECTION2
    data = q.getOneAssignment(assignment_id)
    if data is not None:
        # data.pop('_id')
        return json.loads(json_util.dumps(data)), 200
    else:
        return "assignment not found", 404


# UPLOAD ONE ASSIGNMENT
@app.route('/assignment', methods=['POST'])
def api_setassignment():
    assignment_data = request.json
    q = mc.Query(db.client)
    q.database = DATABASE
    q.collection = COLLECTION2
    response = q.insertOneAssignment(assignment_data)
    if response == 2:
        return "updated existing assignment", 200
    else:
        return "assignment set", 200


def manual_file_setassignment(path):
    """
    not part of API, just here for testing purposes
    """
    db = mc.DB_Connection(addr=CLUSTER)
    db.connect_Client()
    assignment_data = path
    q = mc.Query(db.client)
    q.database = DATABASE
    q.collection = COLLECTION2
    response = q.insertAssighmentFromFile(assignment_data)
    if response == 2:
        return "updated existing assignment", 200
    else:
        return "assignment set", 200

"""
@app.route('/mark', methods=['GET'])
def api_getmark():
    attempt_id = request.headers.get('AttemptID')
    assignment_id = request.headers.get('AssignmentID')
    section_id = request.headers.get('SectionID')
    q = mc.Query(db.client)
    q.database = DATABASE
    q.collection = COLLECTION2
    data = q.getSectionMark(assignment_id)
    if data is not None:
        data.pop('_id')
        # print(data)
        try:
            print()
        except:
            return "not found", 404
        # return json.loads(json_util.dumps(data)), 200
        return "good", 1
    else:
        return "attempt not found", 404
"""

"""
@app.route('/insert-all-attempts', methods=['GET'])
def api_insertattempts():
    if 'path' in request.args:
        path = request.args['path']
    else:
        return "no path supplied", 400
    q = mc.Query(db.client)
    q.database = DATABASE
    q.collection = COLLECTION1
    response = q.insertAllAttempts(path)
    if response == [0]:
        return "error reading file", 403
    elif response == [1]:
        return "attempts uploaded", 200
    else:
        return "some attempts already exist in the database: " + str(response), 200
"""

if __name__ == '__main__':
    db = mc.DB_Connection(addr=CLUSTER)
    db.connect_Client()
    context = ('server.crt', 'server.key')  # certificate and key files
    if HTTPS:
        app.run(host='127.0.0.1', port=5000, debug=True, ssl_context=context)#
    else:
        app.run()

