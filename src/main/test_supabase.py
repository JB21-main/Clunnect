from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Example: fetch rows from an existing table (say "clubs")
try:
    resp = supabase.table("clubs").select("*").execute()
    print("Data:", resp.data)
except Exception as e:
    print("Error:", e)
