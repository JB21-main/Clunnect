from typing import List
from Data import User, Club
from Data.Event import Event
from supabase import create_client, Client
from dotenv import load_dotenv
from Data.Level import Level
import os

print("Loaded DBmgr module from:", __name__)
class DBmgr:
    def __init__(self):
        load_dotenv()
        print("LLoaded DB URL:", os.getenv("DATABASE_URL"))
        
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")

        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Missing Supabase credentials in .env")
        
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Supabase client created successfully!")

    def find_club_by_name(self,query: str):
        response = self.supabase.table("clubs").select("*").ilike("name", f"%{query}%").execute()
        return response.data
    
    def is_club_name_available(self, club_name: str):
        response = self.supabase.table("clubs").select("id").eq("name", club_name).execute()
        return len(response.data) == 0

    def save_club(self, name: str, description: str, owner_id: int, category: str | None = None, meeting_day: str | None = None,
    meeting_time: str | None = None):
        club_data = {
            'name': name,
            'description': description,
            'owner_id': owner_id,
            'category': category,
            'meeting_day' : meeting_day,
            'meeting_time': meeting_time
    }

        response = self.supabase.table("clubs").insert(club_data).execute()
        if response.data:
            return response.data[0]
        return None

    def get_club_list(self):
        response = self.supabase.table("clubs").select("*").execute()
        return response.data if response.data else []
    
    def get_user_clubs(self, user_id: int) -> List[int]:
        print("Hey uhm")
        response = self.supabase.table("club_members").select("club_id").eq("user_id", user_id).execute()
        return [row["club_id"] for row in response.data]
    
    def add_user_to_clubs(self, user_id: int, club_id: int):
        print("attempting to add")
        response = self.supabase.table("club_members").insert({"user_id": user_id, "club_id": club_id}).execute()
        return response.data
    
    def get_user_by_email(self, email:str):
        response = self.supabase.table("users").select("*").eq("email", email).execute()
        data = response.data

        if data and len(data) > 0:
            return data[0]
        return None
    
    def insert_user(self, name: str, email: str, password_hash: str, level=Level.MEMBER):
        data = {
            "username": name,
            "email": email,
            "password_hash": password_hash,
            "level": level
        }
        response = self.supabase.table("users").insert(data).execute()
    
        if response.data:
            return response.data[0]
        return None
    
    #authentication

    def password_by_email(self, email:str):
        response = self.supabase.table("users").select("password_hash").eq("email", email).execute()
        if response.data:
            return response.data[0]["password"]
        return None
    
    def change_account_info(self, user_id: int, new_data: dict):
        #not yet implemented
        return None

    def get_club(self, club_id: int):
        """
        Returns a dict with club fields or None.
        Expects 'clubs' table with columns: id, name, description, owner_id.
        """
        response = self.supabase.table("clubs").select("*").eq("id", club_id).limit(1).execute()
        if getattr(response, "error", None):
            raise Exception(response.error.message)
        if response.data:
            return response.data[0]
        return None

    def update_club(self, club_id: int, name: str = None, description: str = None, category: str = None, date: str = None, time: str = None):
        """
        Partial update. Pass only the fields you want to change.
        """

        updates = {}
        if name is not None:
            updates["name"] = name
        if description is not None:
            updates["description"] = description
        if category is not None:
            updates["category"] = category
        if date is not None:
            updates["meeting_day"] = date
        if time is not None:
            updates["meeting_time"] = time

        if not updates:
            return True  # nothing to do

        response = self.supabase.table("clubs").update(updates).eq("id", club_id).execute()
        print("UPDATES:", updates)
        print("CLUB ID:", club_id)
        print("SUPABASE RESPONSE:", response)

        if getattr(response, "error", None):
            raise Exception(response.error.message)
        return True

    def delete_club(self, club_id: int):
        """
        Hard delete. If you want soft-delete, create a 'deleted_at' column and update instead.
        """
        response = self.supabase.table("clubs").delete().eq("id", club_id).execute()
        if getattr(response, "error", None):
            raise Exception(response.error.message)
        return True

    def find_club_by_owner(self, owner_id: int):
        """
        Find the requesting users owned clubs
        """
        response = self.supabase.table("clubs").select("id, name").eq("owner_id", owner_id).execute()
        return response.data
    
    def insert_event(self, name: str, description: str, category: str, date: str, time: str, club_id: int, owner_id: int):
        event_data = {
            'name': name,
            'description': description,
            'category': category,
            'date': date,
            'time': time,
            'club_id': club_id,
            'owner_id': owner_id
    }

        response = self.supabase.table("events").insert(event_data).execute()
        if response.data:
            return response.data[0]
        return None
    
    def find_event_by_owner(self, owner_id: int):
        """
        Find the requesting users owned clubs
        """
        response = self.supabase.table("events").select("id, name").eq("owner_id", owner_id).execute()
        return response.data
    
    def get_event_by_id(self, event_id):
        """
        Find the event by it's associated ID
        """
        response = self.supabase.table("events").select('*').eq("id", event_id).execute()
        if not response.data:
            return None  # no event found

        row = response.data[0]  # extract the first (and only) row

        event = Event(
            event_id=row["id"],
            name=row["name"],
            description=row.get("description"),
            club_id=row["club_id"],
            date=row["date"],
            time=row["time"]
        )

        return event

    def update_event(self, event_id: int, update_form: dict):
        """

        """
        current_event = self.get_event_by_id(event_id)
        if not current_event:
            return None

        update_values = {}

        for key, value in update_form.items():
            if value is not None and value != "" and getattr(current_event, key, None) != value:
                update_values[key] = value

        if len(update_values) == 0:
            return None

        response = self.supabase.table("events").update(update_values).eq("id", event_id).execute()

        if response.data:
            return response.data[0]

        return None
    
    def delete_event(self, event_id: int):
        try:
            response = self.supabase.table("events").delete().eq("id", event_id).execute()

            if response.data and len(response.data) > 0:
                return True
            return False
        except Exception as e:
            print(f"Error deleting event: {e}")
            return False