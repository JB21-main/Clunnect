class ClubSystem:

    def __init__(self):
        # Use a set so lookups for “does this club already exist?” are O(1)
        self.existing_clubs = set()

    def create_club(self, club_name: str, club_description: str) -> str:

        # 1. Empty / whitespace club name
        if not club_name or club_name.strip() == "":
            return "Club Name cannot be empty"

        # 2. Club name already exists
        if club_name in self.existing_clubs:
            return "A club with this name already exists"

        # 3. Empty / whitespace description
        if not club_description or club_description.strip() == "":
            return "Description cannot be empty"

        # 4. Description too short
        if len(club_description) < 50:
            return "Description must be at least 50 characters"

        # --- All checks passed: create the club ---
        self.existing_clubs.add(club_name)
        return "Club Created Successfully"
