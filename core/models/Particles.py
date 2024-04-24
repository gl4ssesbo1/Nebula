from flask_restful import reqparse
from main import auth, app
from flask_sqlalchemy import SQLAlchemy

from core.Agents.particle_modules import Particles

particle_args = reqparse.RequestParser()
particle_args.add_argument("host", type=str, help="You need to add the host", required=True)
particle_args.add_argument("port", type=int, help="You need to add the port", required=True)
particle_args.add_argument("module", type=str, help="You need to add the module", required=True)

db = SQLAlchemy(app)

@app.route('/api/latest/particles', method=['GET'])
@auth.login_required
def list_particles():
    particles = Particles.query.all()
    return particles

@app.route('/api/latest/particles/<str:id>', method=['POST'])
@auth.login_required
def list_particles(id):
    listener = Particles.query.filter_by(id=id).first()
    return listener

@app.route('/api/latest/particles/<str:id>', method=['PUT'])
@auth.login_required
def list_particles(id):
    args = particle_args.parse_args()
    host = args['host']
    port = args['port']
    module = args['module']

    listener = Particles(
        id=id,
        host=host,
        port=port,
        module=module
    )

    db.add(listener)
    db.commit()

