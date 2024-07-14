from flask import Blueprint, request, Response
from core.database.models import DigitalOceanCredentials
import sys
from flask import Response, request
from flask_jwt_extended import create_access_token, jwt_required
import datetime
import flask_mongoengine
from core.enum_user_privs.getuid_aws import getuid

digitaloceancredentials_blueprint = Blueprint('digitaloceancredentials', __name__)

@digitaloceancredentials_blueprint.route('/api/latest/digitaloceancredentials', methods=['GET'])
@jwt_required()
def list_digitaloceancredentials():
    docredentials = DigitalOceanCredentials.objects().to_json()
    return Response(docredentials, mimetype="application/json", status=200)


@digitaloceancredentials_blueprint.route('/api/latest/digitaloceancredentials/getuid', methods=['POST'])
@jwt_required()
def getuid_digitalocean_credentials():
    body = request.get_json()
    try:
        workspace = body['workspace']

        docredentials = DigitalOceanCredentials.objects.get(digitalocean_profile_name=body.get('digitalocean_profile_name'))

        return {'UserName': getuid(docredentials, workspace)}, 200
    except flask_mongoengine.DoesNotExist:
        return {'error': "Credentials do not exist"}, 404


@digitaloceancredentials_blueprint.route('/api/latest/digitaloceancredentials', methods=['POST'])
@jwt_required()
def get_digitaloceancredentials():
    body = request.get_json()
    try:
        digitaloceancreds = DigitalOceanCredentials.objects.get(digitalocean_profile_name=body.get('digitalocean_profile_name'))

        return {'awscredentials': digitaloceancreds}, 200
    except flask_mongoengine.DoesNotExist:
        return {'error': "Credentials do not exist"}, 404


@digitaloceancredentials_blueprint.route('/api/latest/digitaloceancredentials', methods=['PUT'])
@jwt_required()
def set_digitaloceancredentials():
    body = request.get_json()

    try:
        # aws_creds = DigitalOceanCredentials.objects(**body).save()
        DigitalOceanCredentials(**body).save()
        return {"message": "Credentials of '{}' was created!".format(body['digitalocean_profile_name'])}, 200

    except Exception as e:
        if "Tried to save duplicate unique keys" in str(e):
            return {"error": "Credentials Exist", 'status_code': 1337}

        return {"error": str(e)}, 500


@digitaloceancredentials_blueprint.route('/api/latest/digitaloceancredentials', methods=['DELETE'])
@jwt_required()
def delete_digitaloceancredentials():
    try:
        body = request.get_json()
        digitalocean_profile_name = body['digitalocean_profile_name']
        DigitalOceanCredentials.objects.get_or_404(digitalocean_profile_name=digitalocean_profile_name).delete()
        return {"message": "Credentials of '{}' were deleted!".format(body['digitalocean_profile_name'])}, 200
    except Exception as e:
        return sys.exc_info()[1], 500
