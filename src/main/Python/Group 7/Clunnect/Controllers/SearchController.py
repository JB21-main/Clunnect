from typing import List
from Services.DBmgr import DBmgr
from Data.Club import Club

class SearchController:
    
    def __init__(self, dbmgr: DBmgr):
        self.db = dbmgr

    def search(self, query: str) -> List:
        # Case 1: Handle None or non-string input 
        if query is None or not isinstance(query, str):
            print("SearchController: Invalid input type received.")
            return []

        # Case 2: Clean the input (remove leading/trailing spaces)
        clean_query = query.strip()

        # Case 3: Handle empty strings after cleaning 
        if not clean_query:
            print("SearchController: Query was empty or just whitespace.")
            return []

        try:
            # Case 4: Valid input - Attempt the database search
            results = self.db.find_club_by_name(clean_query)
            
            # Case 5: Handle if DB returns None instead of an empty list
            if results is None:
                return []

            # Case 6: Results found (or empty list if typo/no match)
            return results

        except Exception as e:
            # Case 7: Database connection error or unexpected failure
            print(f"Error during search operation for query '{clean_query}': {e}")
            return []
