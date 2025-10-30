class ClubSystem:
    def __init__(self):
        self.existing_clubs = set()

    def create_club(self, club_name, club_description):
        """
        Processes the creation of a new club based on validation rules.
        Returns a string message indicating success or a specific error.
        
        VALIDATION ORDER IS CRITICAL FOR THE TESTS TO PASS:
        """
        
        # --- VALIDATION BLOCK ---
        
        # 1. Check for empty/whitespace club name.
        if not club_name or club_name.strip() == "":
            return "Club Name cannot be empty"

        # 2. Check if club name already exists.
        if club_name in self.existing_clubs:
            return "A club with this name already exists"

        # 3. Check for empty/whitespace description.
        if not club_description or club_description.strip() == "":
            return "Description cannot be empty"

        # 4. Check for description length.
        if len(club_description) < 50:
            return "Description must be at least 50 characters"

        # --- SUCCESS BLOCK ---
        # If all checks pass, add the club and return success.
        self.existing_clubs.add(club_name)
        return "Club Created Successfully"

