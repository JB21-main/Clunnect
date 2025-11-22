# test_join_club_boundaries.py
import pytest
from Services.DBmgr import DBmgr
from Controllers.JoinClubController import ClubController

@pytest.fixture
def system():
    """Initialize the ClubSystem for testing."""
    dbMgr = DBmgr()
    sys = ClubController(dbMgr)
    return sys


# --- BOUNDARY VALUE TEST CASES --- #
# Sucess!
def test_boundary_successful_join(system):
    """Authorized user joins an existing club successfully — valid boundary."""
    result = system.join_club(user_id="alex", club_name="IEEE", authorized=True)
    assert result == "Successfully joined IEEE."
    assert "alex" in system.clubs["IEEE"]

#User already member
def test_boundary_existing_member(system):
    """User already member — invalid boundary."""
    result = system.join_club(user_id="taylor", club_name="ACM", authorized=True)
    assert result == "You are already a member of ACM."

#Multiple Click
def test_boundary_multiple_clicks(system):
    """Multiple clicks — only one membership record should be created."""
    result1 = system.join_club(user_id="alex", club_name="Gaming Club", authorized=True)
    result2 = system.join_club(user_id="alex", club_name="Gaming Club", authorized=True)
    assert result2 == "Already a member"
    
#Unauthorized user
def test_boundary_unauthorized_user(system):
    """Unauthorized user attempting to join — invalid boundary."""
    result = system.join_club(user_id="alex", club_name="ACM", authorized=False)
    assert result == "User not authorized"

#No existenting club
def test_boundary_nonexistent_club(system):
    """Club name not in the system — invalid boundary."""
    result = system.join_club(user_id="alex", club_name="Chess Club", authorized=True)
    assert result == "Club not found"

#no club selected
def test_boundary_whitespace_club_name(system):
    """Club name not selected— invalid input."""
    result = system.join_club(user_id="alex", club_name="   ", authorized=True)
    assert result == "Club Name not selected"

#club name empty
def test_boundary_empty_club_name(system):
    """Empty club name — invalid input."""
    result = system.join_club(user_id="alex", club_name="", authorized=True)
    assert result == "Club Name cannot be empty"

