import boto3
import botocore

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

clientcommands_blueprint = Blueprint('clientcommands', __name__)

@clientcommands_blueprint.route('/api/latest/clientcommands/get_user_id', methods=['GET'])
@jwt_required()
def aws_get_user_id():
    body = request.get_json()
    profile_dict = body['profile_dict']
    user_agent = body['user_agent']

    region = profile_dict['aws_region']
    access_key_id = profile_dict['aws_access_key']
    secret_key = profile_dict['aws_secret_key']
    session_token = ""

    params = {
        "service": "sts",
        "region_name": region,
        "aws_access_key_id": access_key_id,
        "aws_secret_access_key": secret_key,
    }

    if user_agent is not None:
        session_config = botocore.config.Config(user_agent=user_agent)
        params["config"] = session_config

    if "aws_session_token" in profile_dict:
        params["aws_session_token"] = session_token

    try:
        client = boto3.client(
            **params
        )

        response = client.get_caller_identity()

        del response['ResponseMetadata']
        return response

    except Exception as e:
        return {"error": str(e)}

