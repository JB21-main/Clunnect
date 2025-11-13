from typing import List
from Data import User, Club
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

    def save_club(self, name:str,description:str, owner_id: int):
        club_data = {
            'name': name,
            'description': description,
            'owner_id': owner_id
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

    def update_club(self, club_id: int, name: str = None, description: str = None):
        """
        Partial update. Pass only the fields you want to change.
        """
        updates = {}
        if name is not None:
            updates["name"] = name
        if description is not None:
            updates["description"] = description

        if not updates:
            return True  # nothing to do

        response = self.supabase.table("clubs").update(updates).eq("id", club_id).execute()
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

