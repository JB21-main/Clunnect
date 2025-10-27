from werkzeug.security import generate_password_hash
from ..Services import Verifier
from ..Services import ValidationService
from ..Services import SessionManager
from ..Services import UserCreator
from ..Data import Level
from ..Data import User

class AuthController:
    def __init__(self, dbmgr: DBmgr):
        self.verifier = Verifier()
        self.validation = ValidationService()
        self.sessions = SessionManager()
        self.user_creator = UserCreator(dbmgr)
        self.db = dbmgr

    def authenticate(self, email: str, password: str):
        if not self.validation.validate_email(email):
            return False, "Invalid email format"
        
        user = self.db.get_user_by_email(email)

        if not user:
            return False, "An account with that email was not found"
        
        if not self.verifier.validate_password(user["password"], password):
            return False, "Incorrect password"
        
        token = self.sessions.create_session(user)

        user = User(
            user["id"],
            user["name"],
            user["email"],
            Level(user["level"])
        )
        return True, {"token": token, "user":user}
    
    def register(self, name: str, email: str, password:str, level=Level.MEMBER)
        user = self.user_creator.create_user(name,email,password,level.value)

        token = self.sessions.create_session(user.ID)

        return True, {"user": user, "token": token}
    
    def logout(self, token:str):
        self.sessions.destroy_session(token)
        return True
    

