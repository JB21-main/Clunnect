# join_club.py

class ClubSystem:
    def __init__(self):
        # Simulate database of clubs and members
        self.clubs = {
            "ACM": {"taylor"},   # preload existing club and member
            "IEEE": set(),
            "Robotics": set()
        }

    def join_club(self, user_id, club_name, authorized=True):
        """
        Handles Join Club logic.
        Returns string messages for success, invalid, or exceptional outcomes.
        """

        # 1 Authorization Check
        if not authorized:
            return "User not authorized"

        # 2 Validate club name
        if not club_name or str(club_name).strip() == "":
            return "Club Name cannot be empty"

        # 3️ Check if club exists
        if club_name not in self.clubs:
            return "Club not found"

        # 4️ Check if user is already a member
        if user_id in self.clubs[club_name]:
            return f"You are already a member of {club_name}."

        # 5️ Add user (simulate database insert)
        self.clubs[club_name].add(user_id)
        return f"Successfully joined {club_name}."
