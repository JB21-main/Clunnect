from Services.DBmgr import DBmgr

print("Loaded CalendarController module from:", __name__)

class CalendarController:
    def __init__(self, dbmgr: DBmgr):
        self.db = dbmgr

    def get_all_events(self):
        try:
            events = self.db.get_all_events()
            if events:
                return True, events
            else:
                return False, "No events found."
        except Exception as e:
            print("Error fetching events:", e)
            return False, f"Error: {str(e)}"

    
