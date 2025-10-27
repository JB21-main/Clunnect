import re

class ValidationService:
    
    min_password_length = 7

    def validation_email(self, email:str) -> bool:
        """Checks if the email follows valid email structure(IE: name@domain.TLD)
        
        Args:
            email (str): The user's email input.

        Returns:
            bool: True if the email follows the valid format
        """
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
    
    def validate_password(self, password:str):
        """Checks if the password is longer than the minimum input
        
        Args:
            password (str): The user's password input.

        Returns:
            bool: True if the password is longer than the minimum length
        """
        return len(password) >= ValidationService.min_password_length
    
    def validate_club_data(self, club:Club):
        """Checks if the club has valid information in all attributes
        
        Args:
            club (Club): The club to validate

        Returns:
            bool: True if the club has a name, category, an int ID, a valid datetime, and a list of members initialized.
        """
        if not club.name or not club.category:
            return False
        
        if not isinstance(club.ID, int) or club.ID < 0:
            return False
        
        from datetime import datetime
        if not isinstance(club.time, datetime):
            return False
        
        if not isinstance(club.members, list) or not all(isinstance(m, int) for m in club.members):
            return False
        
        return True