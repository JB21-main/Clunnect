from Data.Level import Level
from Services.DBmgr import DBmgr

class FacultyController:
    def __init__(self, dbmgr: DBmgr):
        self.db = dbmgr

    def get_user_permission(self, user_id: int):
        """
        Returns level of user
        """
        response = self.db.supabase.table("users").select("level").eq("id", user_id).execute()
        if not response.data:
            return False, "User not found"

        level_value = response.data[0]["level"]
        return True, Level(level_value)

    def set_user_permission(self, user_id: int, level: Level):
        """
        Sets user's permission level
        """
        response = self.db.supabase.table("users") \
            .update({"level": level.value}) \
            .eq("id", user_id) \
            .execute()

        if response.data:
            return True, Level(response.data[0]["level"])
        return False, "Failed to update permission level"
