from flask_jwt_extended import get_jwt_identity
from teamserver.core.database.models import Cosmonaut

def check_user(role):
    curuser = get_jwt_identity()
    print(curuser)
    cosmonaut = Cosmonaut.objects.get(cosmonaut_name=curuser)

    if not role in cosmonaut['roles']:
        return {"error": f"User '{curuser}' needs role '{role}' to execute this command"}

    else:
        return None