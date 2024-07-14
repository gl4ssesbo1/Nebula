import sys

import flask_mongoengine
from flask import Blueprint
from flask import Response, request
from flask_jwt_extended import jwt_required

from core.database.models import Domains

domains_blueprint = Blueprint('domainsblueprint', __name__)

@domains_blueprint.route('/api/latest/domains', methods=['GET'])
@jwt_required()
def list_domains():
    domains = Domains.objects().to_json()
    return Response(domains, mimetype="application/json", status=200)


@domains_blueprint.route('/api/latest/domains', methods=['POST'])
@jwt_required()
def get_domain():
    body = request.get_json()
    try:
        domains = Domains.objects.get(dn_name=body['dn_name'])

        return {'dn_name': domains}, 200
        
    except flask_mongoengine.DoesNotExist:
        return {'error': "Credentials do not exist"}, 404

