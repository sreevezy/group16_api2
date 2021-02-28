import pymongo
import logging
import os
import bson
import json
import jsonref
import re
from bson.objectid import ObjectId


class DB_Connection:
    """
    connection object
    """

    def __init__(self, addr=None):
        self.address = addr
        self.port = 27017
        #27017 is default port for mongodb
        self.client = None

    def connect_Client(self):
        try:
            print(self.address)
            print(self.port)
            self.client = pymongo.MongoClient(self.address)
        except:
            logging.error("couldn't connect to address given")


class Query:
    """"
    query object.
    an instance of DB_connection is passed in upon an instance of Query's creation
    """
    database = 'webpage'
    collection = None
    payloadKey = "payloadKeyNotInherited"

    def __init__(self, client_in):
        self.client = client_in

    def insertAllAttempts(self, filepath):
        failed_docs = []
        with open(filepath, 'r') as document:
            try:
                contents = document.read()
                content_structure = json.loads(contents)
                self.database = content_structure["AssignmentName"]
            except:
                return [0]
        for attempt in content_structure['Attempts']:

            location = self.client[self.database][self.collection]

            if not(location.find_one({'name': attempt["name"]})):
                location.insert_one(attempt)
            else:
                failed_docs.append(attempt["name"])
        if len(failed_docs) > 0:
            return failed_docs
        else:
            return [1]

    def insertAssighmentFromFile(self, filepath):
        failed_docs = []
        with open(filepath, 'r') as document:
            try:
                contents = document.read()
                #content_structure = json.loads(contents)
                self.database = "test_main"
            except:
                return [0]

        self.insertOneAssignment(contents)


    def getOneAttempt(self, identifier):
        location = self.client[self.database][self.collection]
        payload = location.find_one({'AttemptID': identifier})
        return payload

    def insertOneAttempt(self, attempt):
        location = self.client[self.database][self.collection]
        if not (location.find_one({'AttemptID': attempt["AttemptID"]})):
            location.insert_one(attempt)
            return 1
        else:
            location.delete_one({'AttemptID': attempt["AttemptID"]})
            location.insert_one(attempt)
            return 2


    def deleteOneAttempt(self, attempt_id):
        location = self.client[self.database][self.collection]
        if not (location.find_one({'AttemptID': attempt_id})):
            return 0
        else:
            location.delete_one({'AttemptID': attempt_id})
            return 1


    def insertOneAssignment(self, assignment):
        json_assignment = json.loads(assignment)
        location = self.client[self.database][self.collection]
        if not (location.find_one({'AssignmentID': json_assignment["AssignmentID"]})):
            location.insert_one({'AssignmentID': json_assignment["AssignmentID"], 'Assignment_content' : bson.encode(json_assignment)})
            return 1
        else:
            location.delete_one({'AssignmentID': json_assignment["AssignmentID"]})
            self.insertOneAssignment(assignment)
            return 2


    def getOneAssignment(self, identifier):
        location = self.client[self.database][self.collection]
        payload = location.find_one({"AssignmentID": int(identifier)})
        if payload is not None:
            content = bson.decode(payload["Assignment_content"])
            return content
        #doublestr = re.sub('\'', '\"', f"{content}")
        #doublestr = re.sub('None', 'null', doublestr)
        return None

    """
    def getSectionMark(self, identifier):
        location = self.client[self.database][self.collection]
        payload = location.find({'AssignmentID': identifier}, {'GivenMark' 1})
        return payload
    """

    def updateCommentBank(self):
        pass