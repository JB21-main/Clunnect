from Services.DBmgr import DBmgr
from werkzeug.security import generate_password_hash  # Used for hashing the new password

class AccountController:
    
    def __init__(self, dbmgr: DBmgr):
        self.db = dbmgr

    def change_account_info(self, username: str, new_pass: str, user_id: int):
        new_data = {}
        if username and username.strip():
            new_data["username"] = username.strip()

        if new_pass and new_pass.strip():
            new_data["password_hash"] = generate_password_hash(new_pass)
        
        if not new_data:
            return False, "No new information was provided to update."

        try:
            success = self.db.change_account_info(user_id, new_data)
            
            if success:
                return True, "Account information updated successfully."
            else:
                return False, "Failed to update account information."
                
        except Exception as e:
            print(f"Error in AccountController.change_account_info: {e}")
            return False, f"An error occurred: {e}"