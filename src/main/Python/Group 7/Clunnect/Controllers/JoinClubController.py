from Data.Club import Club
from Services.DBmgr import DBmgr

class JoinClubController:
  
    def __init__(self, dbmgr: DBmgr):
        self.db = dbmgr

    def join_club(self, userID: int, club: Club) -> str:
        # basic validation
        if not isinstance(userID, int) or userID <= 0:
            return "Invalid user"
        if not isinstance(club, Club) or club.club_id is None:
            return "Invalid club"

        club_id = club.club_id

        # If owner is implicitly a member, we can short-circuit
        if getattr(club, "owner_id", None) == userID:
            return "Already a member"

        # Check if user already in this club using DBmgr.get_user_clubs
        try:
            existing_clubs = self.db.get_user_clubs(userID)  # returns List[int] of club_ids
        except Exception as e:
            return f"Error checking membership: {e}"

        if club_id in existing_clubs:
            return "Already a member"

        # Add membership row using DBmgr.add_user_to_clubs
        try:
            self.db.add_user_to_clubs(userID, club_id)
            return "Joined successfully"
        except Exception as e:
            return f"Error joining club: {e}"
