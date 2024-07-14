import sys
import boto3
import botocore

import flask_mongoengine
from flask import Blueprint, request, Response
from core.database.models import Cosmonaut
import sys
from flask import Response, request
from flask_jwt_extended import create_access_token, jwt_required
import datetime
import json

clientcommands_blueprint = Blueprint('clientcommands', __name__)

@clientcommands_blueprint.route('/api/latest/clientcommands', methods=['GET'])
@jwt_required()
def aws_get_user_id(profile_dict, user_agent):
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
