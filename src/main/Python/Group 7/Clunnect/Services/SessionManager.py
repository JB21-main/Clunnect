import secrets
from Services import DBmgr

class SessionManager:
    sessions = {}

    def create_session(self, user_id:int) -> str:
        """Creates a session based on the users id
        
        Args:
            user_id (int): The users ID.

        Returns:
            token (str): the token for the session
        """
        token = secrets.token_urlsafe(32)
        self.sessions[token] = user_id
        return token

    def get_user_by_token(self, token:str):
        """gets the user id based on the given token
        
        Args:
            token (str): the token for the session

        Returns:
            user_id (int): The users ID.
        """
        return self.sessions.get(token)
        
    def destroy_session(self, token: str): 
        """Destroys the session removing it from the list
        
        Args:
            token (str): the token for the session
        """   
        if token in self.sessions:
            del self.sessions[token]