from typing import List
from datetime import datetime

class Club:
    def __init__(self, club_id: int, name: str, description: str, owner_id: int,
        category: str | None = None, meeting_day: str | None = None, meeting_time: str | None = None):

        self.club_id = club_id
        self.name = name
        self.description = description
        self.owner_id = owner_id

        # new fields
        self.category = category or ""
        self.meeting_day = meeting_day or ""
        self.meeting_time = meeting_time or ""

        self.members: List[int] = []  # stores user_ids
        self.events: List[int] = []   # stores event_ids

    def create_club(self, inputData: dict):
        self.name = inputData.get("name", "")
        self.category = inputData.get("category", "")
        self.meeting_time = inputData.get("meeting_time", "")
        self.description = inputData.get("description", "")

    
    def join_request(self, user_id: int):
        #to be added later
        return True
    
    def accept_request(self, user_id:int):
        if user_id not in self.members:
            self.members.append(user_id)