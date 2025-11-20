from typing import List
from datetime import datetime

class Club:
    def __init__(self, club_id:int,name: str, description: str, owner_id: int):
        self.club_id = club_id
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.members: List[int] = [] #stores user_ids
        self.events: List[int] = [] #stores event_ids

    def create_club(self, inputData: dict):

        self.name = inputData.get("name", "")
        self.category = inputData.get("category", "")
        self.description = inputData.get("description", "")
    
    def join_request(self, user_id: int):
        #to be added later
        return True
    
    def accept_request(self, user_id:int):
        if user_id not in self.members:
            self.members.append(user_id)