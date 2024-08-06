import sys

import flask_mongoengine
from flask import Blueprint
from flask import Response, request
from flask_jwt_extended import jwt_required

from core.database.models import AWSS3Bucket

awsbuckets_blueprint = Blueprint('awsbuckets', __name__)

@awsbuckets_blueprint.route('/api/latest/awsbuckets', methods=['GET'])
@jwt_required()
def list_awsbuckets():
    awsbuckets = AWSS3Bucket.objects().to_json()
    return Response(awsbuckets, mimetype="application/json", status=200)

@awsbuckets_blueprint.route('/api/latest/awsbuckets', methods=['POST'])
@jwt_required()
def get_awsbuckets():
    body = request.get_json()
    try:
        awsbuckets = AWSS3Bucket.objects.get(aws_s3_bucket_name=body.get('aws_s3_bucket_name'))

        return {'aws_s3_bucket_name': awsbuckets}, 200
    except flask_mongoengine.DoesNotExist:
        return {'error': "Bucket do not exist"}, 404

