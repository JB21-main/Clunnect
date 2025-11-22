from werkzeug.security import generate_password_hash
from Services.Verifier import Verifier
from Services.ValidationService import ValidationService
from Services.SessionManager import SessionManager
from Services.UserCreator import UserCreator
from Data.Level import Level
from Data.User import User
from Services.DBmgr import DBmgr


print("Loaded AuthController module from:", __name__)
class AuthController:
    def __init__(self, dbmgr: DBmgr):
        self.sessions = SessionManager()
        print("ball")
        self.db = dbmgr

    def authenticate(self, email: str, password: str):
        if not ValidationService.validate_email(email):
            print("invalid?")
            return {"success": False, "error": "Invalid email format"}
        
        user = self.db.get_user_by_email(email)

        print(user)
        if not user:
            return {"success": False, "error": "An account with that email was not found"}
        
        if not Verifier.validate_password(user["password_hash"], password):
            return {"success": False, "error": "Incorrect password"}
        
        token = self.sessions.create_session(user)

        # Took off using ID for now
        user_data = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "level": user["level"]
        }
        return {"success": True, "data": {"token": token, "user":user_data}}
    
    def register(self, name: str, email: str, password:str, level=Level.MEMBER):
        try:
            user = UserCreator(self.db).create_user(name,email,password,level.value)
            token = self.sessions.create_session(user.user_id)
            return True, {"user": user, "token": token}
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, "An unexpected error occurred: " + str(e)
    
    def logout(self, token:str):
        self.sessions.destroy_session(token)
        return True