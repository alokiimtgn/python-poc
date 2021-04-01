import flask
from flask import request, jsonify
class response: 
    @staticmethod   
    def sendResponse(query_parameters):
        return jsonify(query_parameters)