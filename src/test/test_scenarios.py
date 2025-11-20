import pytest
import os
import sys

# --- Make sure we can import from src/main ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))      # .../mangage_clubs/src
MAIN_DIR = os.path.join(BASE_DIR, "main")                  # .../mangage_clubs/src/main

if MAIN_DIR not in sys.path:
    sys.path.insert(0, MAIN_DIR)

from club_system import ClubSystem


@pytest.fixture
def system():
    s = ClubSystem()
    s.existing_clubs.add("ACM")
    return s


# ---------------- SCENARIO TESTS (VALID / INVALID / EXCEPTIONAL) ----------------

def test_scenario_1_valid_valid(system):
    """
    Valid name + valid description.
    Expect: club is created successfully and added to existing_clubs.
    """
    result = system.create_club(
        "HackUTD",
        "The official hackathon of UTD, providing workshops, resources, "
        "and innovation opportunities for students."
    )
    assert result == "Club Created Successfully"
    assert "HackUTD" in system.existing_clubs


def test_scenario_2_valid_invalid_description(system):
    """
    Valid name + invalid (too short) description.
    """
    result = system.create_club("UTDAI", "AI club.")
    assert result == "Description must be at least 50 characters"


def test_scenario_3_valid_exceptional_description_empty(system):
    """
    Valid name + empty description.
    """
    result = system.create_club("Women in CS", "")
    assert result == "Description cannot be empty"


def test_scenario_4_invalid_name_exists_valid_desc(system):
    """
    Name already exists (ACM) + valid description.
    """
    result = system.create_club(
        "ACM",
        "A computing club offering events, study groups, and career help."
    )
    assert result == "A club with this name already exists"


def test_scenario_5_invalid_name_exists_invalid_desc(system):
    """
    Name exists (ACM) + invalid (short) description.
    Name check happens first.
    """
    result = system.create_club("ACM", "Short desc")
    assert result == "A club with this name already exists"


def test_scenario_6_invalid_name_exists_exceptional_desc_empty(system):
    """
    Name exists (ACM) + empty description.
    """
    result = system.create_club("ACM", "")
    assert result == "A club with this name already exists"


def test_scenario_7_exceptional_name_empty_valid_desc(system):
    """
    Empty name + valid description.
    """
    desc = (
        "A competitive gaming organization hosting tournaments and "
        "events for the student body at UTD."
    )
    result = system.create_club("", desc)
    assert result == "Club Name cannot be empty"


def test_scenario_8_exceptional_name_empty_invalid_desc(system):
    """
    Empty name + invalid (short) description.
    Name validation is first.
    """
    result = system.create_club("", "short")
    assert result == "Club Name cannot be empty"


def test_scenario_9_exceptional_name_empty_exceptional_desc(system):
    """
    Empty name + empty description.
    """
    result = system.create_club("", "")
    assert result == "Club Name cannot be empty"
