from typing import Optional
from Data.Club import Club

class ClubController:
    def __init__(self, dbmgr):
        self.db = dbmgr

    # ---------- CREATE ----------
    def create_club(self, name: str, description: str, category: str,meeting_time: str,
    owner_id: int):
        if not name or not description:
            return False, "Club name and description cannot be empty"

        club = Club(
            club_id=None,
            name=name,
            description=description,
            owner_id=owner_id,
            category=category,
            meeting_time=meeting_time,
        )

        try:
            row = self.db.save_club(
                name=club.name,
                description=club.description,
                owner_id=club.owner_id,
                category=club.category,
                meeting_time=club.meeting_time,
            )
            if row and "id" in row:
                club.club_id = row["id"]

            return True, "Club created successfully."
        except Exception as e:
            return False, f"Error creating club: {str(e)}"


    # ---------- EDIT / UPDATE ----------
    def edit_club(
        self,
        club_id: int,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        current_user_id: Optional[int] = None  # optional owner check
    ):
        if name is None and description is None:
            return False, "Nothing to update."

        try:
            # Fetch existing club (and verify ownership if you pass current_user_id)
            row = self.db.get_club(club_id)
            if not row:
                return False, "Club not found."

            if current_user_id is not None and row.get("owner_id") != current_user_id:
                return False, "Not authorized to edit this club."

            if name is not None and not name.strip():
                return False, "Club name cannot be empty."
            if description is not None and not description.strip():
                return False, "Club description cannot be empty."

            self.db.update_club(club_id, name=name, description=description)
            return True, "Club updated successfully."
        except Exception as e:
            return False, f"Error updating club: {str(e)}"

    # ---------- DELETE ----------
    def delete_club(
        self,
        club_id: int,
        *,
        current_user_id: Optional[int] = None,  # optional owner check
        hard: bool = True                       
    ):
        try:
            row = self.db.get_club(club_id)
            if not row:
                return False, "Club not found."

            if current_user_id is not None and row.get("owner_id") != current_user_id:
                return False, "Not authorized to delete this club."

            self.db.delete_club(club_id)
            return True, "Club deleted."
        except Exception as e:
            return False, f"Error deleting club: {str(e)}"
       