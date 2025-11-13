from typing import List
from Services.DBmgr import DBmgr
from Data.Club import Club  

class SearchController:
    
    def __init__(self, dbmgr: DBmgr):
        self.db = dbmgr

    def search(self, query: str) -> List:
        if not query or not query.strip():
            print("SearchController: Received empty query.")
            return []

        try:
            results = self.db.find_club_by_name(query)
            return results
        except Exception as e:
            print(f"Error during search operation for query '{query}': {e}")
            return []