from flask import Blueprint, request, Response
from core.database.models import AWSCredentials
import sys
from flask import Response, request
from flask_jwt_extended import create_access_token, jwt_required
import datetime
import flask_mongoengine
from core.enum_user_privs.getuid_aws import getuid
from core.enum_user_privs.getuid_aws_ssmrole import getuidssmrole

awscredentials_blueprint = Blueprint('awscredentials', __name__)

@awscredentials_blueprint.route('/api/latest/awscredentials', methods=['GET'])
@jwt_required()
def list_awscredentials():
    awscredentials = AWSCredentials.objects().to_json()
    return Response(awscredentials, mimetype="application/json", status=200)

@awscredentials_blueprint.route('/api/latest/awscredentials/getuid', methods=['POST'])
@jwt_required()
def getuid_aws_creds():
    body = request.get_json()
    try:
        workspace = body['workspace']

        awscredentials = AWSCredentials.objects.get(aws_profile_name=body.get('aws_profile_name'))

        return {'UserName': getuid(awscredentials, workspace)}, 200
    except flask_mongoengine.DoesNotExist:
        return {'error': "Credentials do not exist"}, 404

@awscredentials_blueprint.route('/api/latest/awscredentials/getuid/ssmrole', methods=['POST'])
@jwt_required()
def getuid_aws_creds_ssmrole():
    body = request.get_json()
    try:
        workspace = body['workspace']

        all_sessions = body["aws_all_sessions"]
        cred_prof = body["aws_profile_name"]
        workspace = body["workspace"]
        useragent = body["user-agent"]
        web_proxies = body["web_proxies"]

        #awscredentials = AWSCredentials.objects.get(aws_profile_name=body.get('aws_profile_name'))

        #return {'UserName': getuid(awscredentials, workspace)}, 200
        return {'UserName': getuidssmrole(all_sessions, cred_prof, useragent, web_proxies)}, 200
    except flask_mongoengine.DoesNotExist:
        return {'error': "Credentials do not exist"}, 404

@awscredentials_blueprint.route('/api/latest/awscredentials', methods=['POST'])
@jwt_required()
def get_awscredentials():
    body = request.get_json()
    try:
        awscredentials = AWSCredentials.objects.get(aws_profile_name=body.get('aws_profile_name'))

        return {'awscredentials': awscredentials}, 200
    except flask_mongoengine.DoesNotExist:
        return {'error': "Credentials do not exist"}, 404


@awscredentials_blueprint.route('/api/latest/awscredentials', methods=['PUT'])
@jwt_required()
def set_awscredentials():
    body = request.get_json()

    try:
        # aws_creds = AWSCredentials.objects(**body).save()
        aws_creds = AWSCredentials(**body).save()
        return {"message": "Credentials of '{}' was created!".format(body['aws_profile_name'])}, 200

    except Exception as e:
        if "Tried to save duplicate unique keys" in str(e):
            return {"error": "Credentials Exist", 'status_code': 1337}

        return {"error": str(e)}, 500


@awscredentials_blueprint.route('/api/latest/awscredentials', methods=['DELETE'])
@jwt_required()
def delete_awscredentials():
    try:
        body = request.get_json()
        aws_profile_name = body['aws_profile_name']
        AWSCredentials.objects.get_or_404(aws_profile_name=aws_profile_name).delete()
        return {"message": "Credentials of '{}' was deleted!".format(body['aws_profile_name'])}, 200
    except Exception as e:
        return {"error": str(e)}, 500
