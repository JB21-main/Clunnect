from Data.Club import Club

class ClubController:
    def __init__(self, dbmgr):
        self.db = dbmgr

    def create_club(self, name: str, description: str, owner_id: int):
        if not name or not description:
            return False, "Club name and description cannot be empty"
        
        club = Club(
            club_id=None,
            name = name,
            description = description,
            owner_id=owner_id
        )
        
        try:
            club.club_id = self.db.save_club(club.name,club.description,club.owner_id)
            return True, "Club created successfully."
        except Exception as e:
            return False, f"Error creating club: {str(e)}"