from werkzeug.security import generate_password_hash
from ValidationService import ValidationService
from ..Data import User

class UserCreator:
    def __init__(self, dbmgr: DBmgr):
        """Initializes the UserCreator with the instance of DBmgr.
        
        Args:
            dbmgr (DBmgr): an instance of the DBmgr object
        """
        self.db = dbmgr
        self.validator = ValidationService()

    def create_user(self, name: str, email: str, password: str, level: str = 'member'):
        """Creates a user using the given name, email, and password
        
        Args:
            name (str): The user's name input
            email (str): The user's email input
            password (str): The user's password input.

        Returns:
            User: returns a created user object with the attributes filled according to the given information
        """
        if not self.validator.validate_email(email):
            raise ValueError("Invalid email format.")
        if not self.validator.validate_password(password):
            raise ValueError("Password is not long enough.")
        
        password_hash = generate_password_hash(password)

        result = self.db.insert_user(name, email, password_hash, level)

        user_id = result[0]["id"] if result else None
        return User(user_id, name, email)