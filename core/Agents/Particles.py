import http.server
import sys
from flask import Blueprint, request, Response
from databases.models import Listeners

particle_blueprint = Blueprint('particles', __name__)

#auth = HTTPBasicAuth()

@particle_blueprint.route('/api/latest/particles', methods=['GET'])
def list_particles():
    particles = Listeners.objects().to_json()
    return Response(particles, mimetype="application/json", status=200)

@particle_blueprint.route('/api/latest/particles/<string:id>', methods=['POST'])
def get_particle(id):
    particle = Listeners.objects.get_or_404(particle_name=id).to_json()
    return Response(particle, mimetype="application/json", status=200)

@particle_blueprint.route('/api/latest/particles', methods=['PUT'])
def set_particle():
    body = request.get_json()
    host = body['host']
    port = int(body['port'])

#@auth.login_required
@particle_blueprint.route('/api/latest/particles/<string:id>', methods=['DELETE'])
def delete_particle(id):
    try:

        Listeners.objects.get_or_404(particle_name=id).delete()
        return '', 200
    except:
        return sys.exc_info()[1], 500