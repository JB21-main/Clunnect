from typing import List
from Data.Level import Level

class User:
    def __init__(self, user_id, name: str, email:str, level=Level.MEMBER):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.level = level
        self.clubs: List[int] = [] #storing club_ids

    def get_user_permission_level(self) -> Level:
        return self.level