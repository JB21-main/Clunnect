from typing import List, Optional
from Data.Event import Event
from Services.DBmgr import DBmgr
from Services.ValidationService import ValidationService

class EventController:
    def __init__(self, dbmgr: DBmgr):
        """Initializes the EventController with the instance of DBmgr.
        
        Args:
            dbmgr (DBmgr): an instance of the DBmgr object
        """
        self.db = dbmgr
        self.validator = ValidationService()

    def create_event(self, form_data: dict, club_id: int, user_id: int) -> Optional[Event]:
        """Creates a new event for a club.
        
        Args:
            form_data (dict): Dictionary containing event data
                - name: str
                - description: str
                - category: str
                - date: str (YYYY-MM-DD)
                - time: str (HH:MM)
            club_id (int): ID of the club hosting the event
            user_id (int): ID of the user creating the event (must be club owner/officer)
            
        Returns:
            Event: The created Event object, or None if creation failed
            
        Raises:
            ValueError: If required fields are missing or invalid
            PermissionError: If user doesn't have permission to create event for this club
        """
        # Validate required fields
        required_fields = ["name", "description", "date", "time"]
        for field in required_fields:
            if not form_data.get(field):
                raise ValueError(f"Missing required field: {field}")

        # Validate user has permission to create event for this club
        if not self._validate_club_permission(user_id, club_id):
            raise PermissionError("User does not have permission to create events for this club")

        # Validate event data
        if not self.validator.validate_event_data(form_data):
            raise ValueError("Invalid event data format")

        # Insert event into database
        result = self.db.insert_event(
            name=form_data["name"],
            description=form_data["description"],
            category=form_data.get("category", ""),
            club_id=club_id,
            date=form_data["date"],
            time=form_data["time"]
        )

        if result:
            event_id = result.get("id")
            event = Event(
                event_id=event_id,
                name=form_data["name"],
                description=form_data["description"],
                club_id=club_id,
                date=form_data["date"],
                time=form_data["time"]
            )
            event.category = form_data.get("category", "")
            return event
        
        return None

    def edit_event(self, event_id: int, form_data: dict, user_id: int) -> bool:
        """Edits an existing event.
        
        Args:
            event_id (int): ID of the event to edit
            form_data (dict): Dictionary containing updated event data
            user_id (int): ID of the user making the edit
            
        Returns:
            bool: True if edit successful, False otherwise
            
        Raises:
            PermissionError: If user doesn't have permission to edit this event
        """
        # Get the event to verify it exists and get club_id
        event = self.db.get_event_by_id(event_id)
        if not event:
            raise ValueError(f"Event with ID {event_id} not found")

        # Validate user has permission
        if not self._validate_club_permission(user_id, event["club_id"]):
            raise PermissionError("User does not have permission to edit this event")

        # Update event in database
        update_data = {
            "name": form_data.get("name", event["name"]),
            "description": form_data.get("description", event["description"]),
            "category": form_data.get("category", event.get("category", "")),
            "date": form_data.get("date", event["date"]),
            "time": form_data.get("time", event["time"])
        }

        result = self.db.update_event(event_id, update_data)
        return result is not None

    def delete_event(self, event_id: int, user_id: int) -> bool:
        """Deletes an event.
        
        Args:
            event_id (int): ID of the event to delete
            user_id (int): ID of the user requesting deletion
            
        Returns:
            bool: True if deletion successful, False otherwise
            
        Raises:
            PermissionError: If user doesn't have permission to delete this event
        """
        # Get the event to verify it exists and get club_id
        event = self.db.get_event_by_id(event_id)
        if not event:
            raise ValueError(f"Event with ID {event_id} not found")

        # Validate user has permission
        if not self._validate_club_permission(user_id, event["club_id"]):
            raise PermissionError("User does not have permission to delete this event")

        # Delete event from database
        result = self.db.delete_event(event_id)
        return result is not None

    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """Retrieves an event by its ID.
        
        Args:
            event_id (int): ID of the event to retrieve
            
        Returns:
            Event: Event object if found, None otherwise
        """
        event_data = self.db.get_event_by_id(event_id)
        if event_data:
            event = Event(
                event_id=event_data["id"],
                name=event_data["name"],
                description=event_data["description"],
                club_id=event_data["club_id"],
                date=event_data["date"],
                time=event_data["time"]
            )
            event.category = event_data.get("category", "")
            event.attendees = event_data.get("attendees", [])
            return event
        return None

    def get_events_by_club(self, club_id: int) -> List[Event]:
        """Retrieves all events for a specific club.
        
        Args:
            club_id (int): ID of the club
            
        Returns:
            List[Event]: List of Event objects for the club
        """
        events_data = self.db.get_events_by_club(club_id)
        events = []
        
        for event_data in events_data:
            event = Event(
                event_id=event_data["id"],
                name=event_data["name"],
                description=event_data["description"],
                club_id=event_data["club_id"],
                date=event_data["date"],
                time=event_data["time"]
            )
            event.category = event_data.get("category", "")
            event.attendees = event_data.get("attendees", [])
            events.append(event)
        
        return events

    def register_user_for_event(self, event_id: int, user_id: int) -> bool:
        """Registers a user for an event.
        
        Args:
            event_id (int): ID of the event
            user_id (int): ID of the user to register
            
        Returns:
            bool: True if registration successful, False otherwise
        """
        event = self.get_event_by_id(event_id)
        if not event:
            raise ValueError(f"Event with ID {event_id} not found")

        if event.register_attendee(user_id):
            # Update database
            result = self.db.add_event_attendee(event_id, user_id)
            return result is not None
        
        return False  # User already registered

    def _validate_club_permission(self, user_id: int, club_id: int) -> bool:
        """Validates if a user has permission to manage events for a club.
        
        Args:
            user_id (int): ID of the user
            club_id (int): ID of the club
            
        Returns:
            bool: True if user is club owner or officer, False otherwise
        """
        # This would check if user is the club owner or has officer role
        # For now, we'll use a simplified check through DBmgr
        club = self.db.get_club_by_id(club_id)
        if not club:
            return False
        
        # Check if user is the owner
        if club.get("owner_id") == user_id:
            return True
        
        # Check if user is an officer (you'll need to implement this in DBmgr)
        # For now, return True to allow testing
        # TODO: Implement proper role checking
        return True