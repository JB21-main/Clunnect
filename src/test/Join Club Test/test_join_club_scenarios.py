# test_join_club_scenarios.py
import pytest
from join_club import ClubSystem


@pytest.fixture
def system():
    """Set up the test environment with clubs and members."""
    sys = ClubSystem()
    return sys


# --- SCENARIO TEST CASES (UC3 – Join Club) --- #

#Success
def test_case_1_valid(system):
    """Case 1: Valid club, authorized, new member."""
    result = system.join_club(user_id="alex", club_name="ACM", authorized=True)
    assert result == "Successfully joined ACM."
    assert "alex" in system.clubs["ACM"]

#User already member
def test_case_2_already_member(system):
    """Case 2: Valid club, already a member."""
    result = system.join_club(user_id="taylor", club_name="ACM", authorized=True)
    assert result == "You are already a member of ACM."

#Unauthorized user
def test_case_3_unauthorized(system):
    """Case 3: Valid club, unauthorized user."""
    result = system.join_club(user_id="alex", club_name="ACM", authorized=False)
    assert result == "User not authorized"

#No existenting club
def test_case_4_nonexistent_club(system):
    """Case 4: Invalid club (does not exist)."""
    result = system.join_club(user_id="alex", club_name="Chess Club", authorized=True)
    assert result == "Club not found"

#no club selected
def test_case_5_whitespace_name(system):
    """Case 6: Exceptional (Club not selected)."""
    result = system.join_club(user_id="alex", club_name="   ", authorized=True)
    assert result == "Club Name not selected"

#club name empty
def test_case_6_empty_name(system):
    """Case 5: Exceptional (empty club name)."""
    result = system.join_club(user_id="alex", club_name="", authorized=True)
    assert result == "Club Name cannot be empty"
