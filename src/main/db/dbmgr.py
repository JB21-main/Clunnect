from supabase import create_client, Client
from dotenv import load_dotenv
import os

class DBMgr:
    def __init__(self):
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(url, key)

    # UC1: Create a club
    def create_club(self, club_name: str, description: str, creator_id: int):
        data = {
            "name": club_name,
            "description": description,
            "created_by": creator_id
        }
        response = self.client.table("clubs").insert(data).execute()
        return response.data

    # UC3: Join a club
    def join_club(self, user_id: int, club_id: int):
        data = {"user_id": user_id, "club_id": club_id}
        response = self.client.table("user_clubs").insert(data).execute()
        return response.data

    # Optional helper: Get all clubs
    def get_all_clubs(self):
        response = self.client.table("clubs").select("*").execute()
        return response.data
