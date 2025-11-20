import os
import sys
import pytest

# --- Make sure we can import club_system.py from src/main ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))      # .../mangage_clubs/src
MAIN_DIR = os.path.join(BASE_DIR, "main")                  # .../mangage_clubs/src/main

if MAIN_DIR not in sys.path:
    sys.path.insert(0, MAIN_DIR)

from club_system import ClubSystem


@pytest.fixture
def system():
    """Sets up a new system and pre-loads 'ACM' as an existing club."""
    s = ClubSystem()
    valid_desc = (
        "The Association for Computing Machinery at UTD, focusing on CS events."
    )
    s.existing_clubs.add("ACM")
    s.clubs["ACM"] = valid_desc
    return s


# --- Concrete Scenario Test Cases for create_club (Valid / Invalid / Exceptional) ---

def test_case_1_valid_valid(system):
    # (Valid Name, Valid Description)
    club_name = "HackUTD"
    description = (
        "The official student-run hackathon at UTD, organizing events and "
        "innovation opportunities for students."
    )
    result = system.create_club(club_name, description)

    assert result == "Club Created Successfully"
    assert club_name in system.existing_clubs
    assert club_name in system.clubs


def test_case_2_valid_invalid_desc_short(system):
    # (Valid Name, Invalid Description - too short)
    club_name = "UTDAI"
    description = "A club for AI."  # clearly < 50 chars
    result = system.create_club(club_name, description)

    assert result == "Description must be at least 50 characters"


def test_case_3_valid_exceptional_desc_empty(system):
    # (Valid Name, Exceptional Description - empty string)
    club_name = "Women in CS"
    description = ""
    result = system.create_club(club_name, description)

    assert result == "Description cannot be empty"


def test_case_4_invalid_name_exists_valid_desc(system):
    # (Invalid Name - already exists, Valid Description)
    club_name = "ACM"  # preloaded in fixture
    description = (
        "The Association for Computing Machinery. We aim to foster a strong "
        "community for computer science students through events and resources."
    )
    result = system.create_club(club_name, description)

    assert result == "A club with this name already exists"


def test_case_5_invalid_name_exists_invalid_desc(system):
    # (Invalid Name - already exists, Invalid Description - too short)
    club_name = "ACM"  # preloaded
    description = "Another CS club."
    result = system.create_club(club_name, description)

    # Name conflict is checked before description length
    assert result == "A club with this name already exists"


def test_case_6_invalid_name_exists_exceptional_desc_empty(system):
    # (Invalid Name - already exists, Exceptional Description - empty)
    club_name = "ACM"
    description = ""
    result = system.create_club(club_name, description)

    # Name conflict still wins
    assert result == "A club with this name already exists"


def test_case_7_exceptional_name_empty_valid_desc(system):
    # (Exceptional Name - empty, Valid Description)
    club_name = ""
    description = (
        "A new club for students interested in competitive video gaming and "
        "e-sports tournaments on campus."
    )
    result = system.create_club(club_name, description)

    assert result == "Club Name cannot be empty"


def test_case_8_exceptional_name_empty_invalid_desc(system):
    # (Exceptional Name - empty, Invalid Description - short)
    club_name = ""
    description = "e-sports"
    result = system.create_club(club_name, description)

    # Name is validated before description
    assert result == "Club Name cannot be empty"


def test_case_9_exceptional_name_empty_exceptional_desc_empty(system):
    # (Exceptional Name - empty, Exceptional Description - empty)
    club_name = ""
    description = ""
    result = system.create_club(club_name, description)

    assert result == "Club Name cannot be empty"


# --- Additional scenario tests for update_club and delete_club ---

def test_case_10_update_existing_club_valid(system):
    """Happy-path scenario for editing an existing club."""
    new_description = (
        "Updated ACM description focusing on new workshops, mentoring, and "
        "career-building events for CS students."
    )

    result = system.update_club("ACM", new_description)

    assert result == "Club Updated Successfully"
    assert system.clubs["ACM"] == new_description


def test_case_11_delete_existing_club(system):
    """Happy-path scenario for deleting an existing club."""
    result = system.delete_club("ACM")

    assert result == "Club Deleted Successfully"
    assert "ACM" not in system.existing_clubs
    assert "ACM" not in system.clubs
