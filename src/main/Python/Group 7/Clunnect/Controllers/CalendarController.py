from Services.DBmgr import DBmgr

class CalendarController:
    def __init__(self, dbmgr: DBmgr):
        self.db = dbmgr

    def load_calendar_view(self, user_id: int):
        """
        Returns all events for clubs the user is a member of
        """

        # get club_ids of user's clubs
        club_ids = self.db.get_user_clubs(user_id)

        try:
            club_ids = [int(cid) for cid in club_ids]
        except:
            club_ids = []

        if not club_ids:
            return True, []

        response = (
            self.db.supabase
                .table("events")
                .select("*")
                .in_("club_id", club_ids)
                .execute()
        )

        events = response.data if response.data else []

        # format events
        formatted = []
        for e in events:
            formatted.append({
                "name": e["name"],
                "date": e["date"],
                "time": e["time"],
                "club_id": e["club_id"]
            })

        return True, formatted
