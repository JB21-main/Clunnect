from werkzeug.security import check_password_hash

class Verifer:
    def validate_password(self, db_password: str, in_password: str) -> bool:
        """Checks the given hashed password against the inputed password
        
        Args:
            db_password (str): The stored hashed password.
            in_password (str): The user's password input.

        Returns:
            bool: True if the passwords match
        """
        return check_password_hash(db_password, in_password)