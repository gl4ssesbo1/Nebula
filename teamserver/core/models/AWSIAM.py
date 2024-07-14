import sys

import flask_mongoengine
from flask import Blueprint
from flask import Response, request
from flask_jwt_extended import jwt_required

from core.database.models import AWSUsers

awsusers_blueprint = Blueprint('awsusers', __name__)

@awsusers_blueprint.route('/api/latest/awsusers', methods=['GET'])
@jwt_required()
def list_awscredentials():
    awsusers = AWSUsers.objects().to_json()
    return Response(awsusers, mimetype="application/json", status=200)

@awsusers_blueprint.route('/api/latest/awsusers', methods=['POST'])
@jwt_required()
def get_awscredentials():
    body = request.get_json()
    try:
        awsusers = AWSUsers.objects.get(aws_username=body.get('aws_username'))

        return {'aws_username': awsusers}, 200
    except flask_mongoengine.DoesNotExist:
        return {'error': "Credentials do not exist"}, 404

