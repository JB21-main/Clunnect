# src/main/club_system.py

class ClubSystem:

    def __init__(self):
        # Original structure used by your existing tests
        self.existing_clubs = set()

        # New structure to also track descriptions (name -> description)
        self.clubs = {}

    # ------------------------------------------------------------------
    # Helper / shared validation
    def _validate_description(self, description: str):
        if not description or description.strip() == "":
            return "Description cannot be empty"

        if len(description) < 50:
            return "Description must be at least 50 characters"

        return None

    # ------------------------------------------------------------------
    # getClubs() in the diagram
    def get_clubs(self):

        return list(self.clubs.items())

    # ------------------------------------------------------------------
    # [User selects "Add Club"] -> createClub(clubData)
    def create_club(self, club_name, club_description):

        # 1. Check for empty/whitespace club name.
        if not club_name or club_name.strip() == "":
            return "Club Name cannot be empty"

        # 2. Check if club name already exists.
        # (uses existing_clubs because your tests pre-load "ACM" there)
        if club_name in self.existing_clubs:
            return "A club with this name already exists"

        # 3. Check for empty/short description.
        desc_error = self._validate_description(club_description)
        if desc_error:
            return desc_error

        # --- SUCCESS BLOCK ---
        # If all checks pass, add the club and return success.
        self.existing_clubs.add(club_name)
        self.clubs[club_name] = club_description
        return "Club Created Successfully"

    # ------------------------------------------------------------------
    # [User selects "Edit Club"] -> updateClub(updatedData)
    def update_club(self, club_name, new_description):

        # 1. Club must exist
        if club_name not in self.existing_clubs:
            return "Club not found"

        # 2. Validate new description
        desc_error = self._validate_description(new_description)
        if desc_error:
            return desc_error

        # 3. Apply update
        self.clubs[club_name] = new_description
        return "Club Updated Successfully"

    # ------------------------------------------------------------------
    # [User selects "Delete Club"] -> deleteClub(clubID) / removeClub(clubID)
    def delete_club(self, club_name):

        # 1. Club must exist
        if club_name not in self.existing_clubs:
            return "Club not found"

        # 2. Remove from both structures
        self.existing_clubs.remove(club_name)
        if club_name in self.clubs:
            del self.clubs[club_name]

        return "Club Deleted Successfully"
