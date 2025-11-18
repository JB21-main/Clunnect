from Services.DBmgr import DBmgr
from Data.Club import Club

print("Loaded FacultyController module from:", __name__)

class FacultyController:
    def __init__(self, dbmgr: DBmgr):
        self.db = dbmgr
    #clubs
    def get_all_clubs(self):
        try:
            clubs = self.db.get_club_list()
            if clubs:
                return True, clubs
            else:
                return False, "No clubs found."
        except Exception as e:
            print("Error retrieving clubs:", e)
            return False, f"Error: {str(e)}"

    def create_club(self, name: str, description: str, owner_id: int):
        if not name or not description:
            return False, "Club name and description cannot be empty."
        
        club = Club(club_id=None, name=name, description=description, owner_id=owner_id)
        try:
            club.club_id = self.db.save_club(club.name, club.description, club.owner_id)
            return True, "Club created successfully."
        except Exception as e:
            print("Error creating club:", e)
            return False, f"Error: {str(e)}"

    def edit_club(self, club_id: int, new_data: dict):
        try:
            updated = self.db.update_club(club_id, new_data)
            if updated:
                return True, "Club updated successfully."
            else:
                return False, "Club not found or no changes made."
        except Exception as e:
            print("Error editing club:", e)
            return False, f"Error: {str(e)}"

    def delete_club(self, club_id: int):
        try:
            deleted = self.db.delete_club(club_id)
            if deleted:
                return True, "Club deleted successfully."
            else:
                return False, "Club not found or could not be deleted."
        except Exception as e:
            print("Error deleting club:", e)
            return False, f"Error: {str(e)}"
    #events
    def get_all_events(self):
        try:
            events = self.db.get_all_events()
            if events:
                return True, events
            else:
                return False, "No events found."
        except Exception as e:
            print("Error retrieving events:", e)
            return False, f"Error: {str(e)}"

    def create_event(self, name: str, date: str, time: str, location: str, club_id: int):
        if not name or not date or not time:
            return False, "Missing required event details."
        
        try:
            new_event = {
                "name": name,
                "date": date,
                "time": time,
                "location": location,
                "club_id": club_id
            }
            created = self.db.save_event(new_event)
            return (True, "Event created successfully.") if created else (False, "Failed to create event.")
        except Exception as e:
            print("Error creating event:", e)
            return False, f"Error: {str(e)}"

    def edit_event(self, event_id: int, new_data: dict):
        try:
            updated = self.db.update_event(event_id, new_data)
            if updated:
                return True, "Event updated successfully."
            else:
                return False, "Event not found or no changes made."
        except Exception as e:
            print("Error editing event:", e)
            return False, f"Error: {str(e)}"

    def delete_event(self, event_id: int):
        try:
            deleted = self.db.delete_event(event_id)
            if deleted:
                return True, "Event deleted successfully."
            else:
                return False, "Event not found or could not be deleted."
        except Exception as e:
            print("Error deleting event:", e)
            return False, f"Error: {str(e)}"
    
    def get_club_by_id(self, club_id: int):
        try:
            club = self.db.get_club_by_id(club_id)
            if club:
                return True, club
            else:
                return False, "Club not found."
        except Exception as e:
            print("Error retrieving club:", e)
            return False, f"Error: {str(e)}"

    def get_event_by_id(self, event_id: int):
        try:
            event = self.db.get_event_by_id(event_id)
            if event:
                return True, event
            else:
                return False, "Event not found."
        except Exception as e:
            print("Error retrieving event:", e)
            return False, f"Error: {str(e)}"
