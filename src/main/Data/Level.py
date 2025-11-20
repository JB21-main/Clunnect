from enum import Enum

class Level(Enum):
    MEMBER = "member"
    OFFICER = "officer"
    FACULTY = "faculty"
    ADMIN = "admin"

    def __str__(self):
        return self.value