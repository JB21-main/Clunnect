class ClubSystem:
    """
    Simple in-memory club management system for UC-18: Manage Club.

    Right now it only implements the "Create Club" behavior with
    validation rules. Existing clubs are stored in a set called
    `existing_clubs`.
    """

    def __init__(self):
        # Use a set so lookups for “does this club already exist?” are O(1)
        self.existing_clubs = set()

    def create_club(self, club_name: str, club_description: str) -> str:
        """
        Create a new club if all validation rules pass.

        Validation rules (ORDER MATTERS):

        1. Club name cannot be empty or whitespace only.
           → "Club Name cannot be empty"

        2. Club name must be unique (not already in existing_clubs).
           → "A club with this name already exists"

        3. Description cannot be empty or whitespace only.
           → "Description cannot be empty"

        4. Description must be at least 50 characters long.
           → "Description must be at least 50 characters"

        On success:
           - The club name is added to existing_clubs
           - Returns "Club Created Successfully"
        """

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
