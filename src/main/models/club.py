class Club:
    def __init__(self, club_id, club_name, description, creator_id):
        self.club_id = club_id
        self.club_name = club_name
        self.description = description
        self.creator_id = creator_id

    def to_dict(self):
        return {
            "club_id": self.club_id,
            "club_name": self.club_name,
            "description": self.description,
            "creator_id": self.creator_id,
        }
