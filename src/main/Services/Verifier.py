from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

class Verifier:
    @staticmethod
    def validate_password(db_password: str, in_password: str) -> bool:
        """Checks the given hashed password against the inputed password
        
        Args:
            db_password (str): The stored hashed password.
            in_password (str): The user's password input.

        Returns:
            bool: True if the passwords match

        !! NOT USING WERKZEUG RIGHT NOW AS OF PRE PHASE 5
        """
        return db_password == in_password