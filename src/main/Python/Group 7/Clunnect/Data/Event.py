from typing import List
from datetime import datetime

class Event:
    def __init__(self, event_id: int, name: str, description: str, club_id: int, date: str, time: str):
        """Initializes an Event object.
        
        Args:
            event_id (int): Unique identifier for the event
            name (str): Name of the event
            description (str): Description of the event
            club_id (int): ID of the club hosting this event
            date (str): Date of the event (YYYY-MM-DD format)
            time (str): Time of the event (HH:MM format)
        """
        self.event_id = event_id
        self.name = name
        self.description = description
        self.club_id = club_id
        self.date = date
        self.time = time
        self.category = ""
        self.attendees: List[int] = []  # stores user_ids of registered attendees

    def create_event(self, input_data: dict):
        """Updates event details from input data.
        
        Args:
            input_data (dict): Dictionary containing event details
                - name: str
                - description: str
                - category: str
                - date: str
                - time: str
        """
        self.name = input_data.get("name", "")
        self.description = input_data.get("description", "")
        self.category = input_data.get("category", "")
        self.date = input_data.get("date", "")
        self.time = input_data.get("time", "")

    def get_details(self) -> dict:
        """Returns event details as a dictionary.
        
        Returns:
            dict: Dictionary containing all event information
        """
        return {
            "event_id": self.event_id,
            "name": self.name,
            "description": self.description,
            "club_id": self.club_id,
            "category": self.category,
            "date": self.date,
            "time": self.time,
            "attendees": self.attendees
        }

    def register_attendee(self, user_id: int) -> bool:
        """Registers a user for the event.
        
        Args:
            user_id (int): ID of the user to register
            
        Returns:
            bool: True if registration successful, False if already registered
        """
        if user_id not in self.attendees:
            self.attendees.append(user_id)
            return True
        return False

    def is_conflict_with(self, other_event: 'Event') -> bool:
        """Checks if this event conflicts with another event.
        
        Args:
            other_event (Event): Another event to check conflict with
            
        Returns:
            bool: True if events conflict (same date and time), False otherwise
        """
        return self.date == other_event.date and self.time == other_event.time
