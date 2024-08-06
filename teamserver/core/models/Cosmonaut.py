import datetime
import json

import flask_mongoengine
from core.database.models import Cosmonaut
from flask import Blueprint
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from termcolor import colored

cosmonaut_blueprint = Blueprint('cosmonauts', __name__)



@cosmonaut_blueprint.route('/api/latest/cosmonauts', methods=['GET'])
@jwt_required()
def list_cosmonauts():
    cosmonauts = json.loads(Cosmonaut.objects().to_json())
    returned_cosmonauts = []

    for cosmonaut in cosmonauts:
        returned_cosmonauts.append(cosmonaut['cosmonaut_name'])

    return {"cosmonauts": returned_cosmonauts}, 200

@cosmonaut_blueprint.route('/api/latest/cosmonauts', methods=['POST'])
def get_cosmonaut():
    body = request.get_json()
    cosmonaut = Cosmonaut.objects.get(cosmonaut_name=body.get('cosmonaut_name'))
    authorized = cosmonaut.check_password(body['cosmonaut_pass'])
    if not authorized:
        return {'error': 'Permission Denied: Email or password is incorrect'}, 401

    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(cosmonaut.cosmonaut_name), expires_delta=expires)
    print(colored(f"[*] User {cosmonaut['cosmonaut_name']} authenticated successfully at {str(datetime.datetime.now())}", "blue"))

    return {'token': access_token}, 200

@cosmonaut_blueprint.route('/api/latest/cosmonauts', methods=['PUT'])
@jwt_required()
def set_cosmonaut():
    body = request.get_json()
    try:
        cosmonaut = Cosmonaut(**body)
        cosmonaut.hash_password()
        cosmonaut.save()

        print(
            colored(f"[*] User '{body['cosmonaut_name']}' was created at {str(datetime.datetime.now())}!", "green")
        )

        return {"message": "User '{}' was created!".format(body['cosmonaut_name'])}, 200
    except Exception as e:
        return {"error":str(e)}, 500

@cosmonaut_blueprint.route('/api/latest/cosmonauts/password', methods=['PATCH'])
@jwt_required()
def reset_cosmonaut_password():
    try:
        body = request.get_json()
        cosmonaut_name = body['cosmonaut_name']
        cosmonaut = Cosmonaut.objects.get(cosmonaut_name=body.get('cosmonaut_name'))
        cosmonaut.modify(cosmonaut_pass=body.get('cosmonaut_pass'))
        cosmonaut.hash_password()
        cosmonaut.save()

        return {"message": "User '{}' was updated!".format(cosmonaut_name)}, 200

    except flask_mongoengine.DoesNotExist:
        return {"error": "User does not exist"}, 404
    except Exception as e:
        return {"error": str(e)}, 500

@cosmonaut_blueprint.route('/api/latest/cosmonauts', methods=['PATCH'])
@jwt_required()
def update_cosmonaut():
    try:
        body = request.get_json()
        cosmonaut_name = body['cosmonaut_name']
        cosmonaut = Cosmonaut.objects.get(cosmonaut_name=body.get('cosmonaut_name'))
        cosmonaut.modify(cosmonaut_pass=body.get('cosmonaut_pass'))
        cosmonaut.hash_password()
        cosmonaut.save()

        print(colored(f"[*] User '{cosmonaut_name}' was updated at {datetime.datetime.now()}!", "light_blue"))
        return {"message": "User '{}' was updated!".format(cosmonaut_name)}, 200


    except flask_mongoengine.DoesNotExist:
        return {"error": "User does not exist"}, 404
    except Exception as e:
        return {"error": str(e)}, 500

@cosmonaut_blueprint.route('/api/latest/cosmonauts', methods=['DELETE'])
@jwt_required()
def delete_cosmonaut():
    try:
        body = request.get_json()
        cosmonaut_name = body['cosmonaut_name']
        Cosmonaut.objects().get(cosmonaut_name=cosmonaut_name).delete()
        print(colored(f"[*] User '{cosmonaut_name}' was deleted at {datetime.datetime.now()}!", "magenta"))
        return {"message": f"User '{cosmonaut_name}' was deleted!"}, 200
    except flask_mongoengine.DoesNotExist:
        return {"error": "User does not exist"}, 404
    except Exception as e:
        return {"error": str(e)}, 500