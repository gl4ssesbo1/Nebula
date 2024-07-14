from .db import db

class Listeners(db.Document):
    listener_name = db.StringField(required=True, unique=True)
    host = db.StringField(required=True)
    port = db.IntField(required=True)
    listener_protocol = db.StringField(required=True)
    listener_jwt_secret = db.StringField(required=True)
    listener_database_host = db.StringField(required=True)
    listener_database_port = db.IntField(required=True)
    listener_database_name = db.StringField(required=True)

class Particles(db.Document):
    particle_id = db.StringField(required=True, unique=True)
    c2_host = db.StringField(required=True)
    c2_port = db.IntField(required=True, unique=True)
    particle_module = db.StringField(required=True)
    particle_listener = db.StringField(required=True)
    particle_api_user = db.StringField(required=True, unique=True)
    particle_api_pass_hash = db.StringField(required=True, unique=True)
    particle_system = db.StringField()
    particle_env = db.StringField()
    particle_uname = db.DictField()
    particle_env_variables = db.DictField()
    particle_init = db.StringField()
    particle_docksock = db.BooleanField()
    particle_disks = db.ListField()
    particle_privileged_docker = db.BooleanField()
    particle_hostname = db.StringField()
    particle_aws_data = db.ListField()
    particle_meta_data = db.DictField()


class Tasks(db.Document):
    task_command = db.StringField(required=True)
    task_particle = db.StringField(required=True)
    task_status = db.BooleanField(required=True)
    task_send_time = db.DateTimeField(required=True)
    task_response_time = db.DateTimeField()
    task_response = db.StringField()
