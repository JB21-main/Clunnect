import pytest
import os
import sys

# --- Make sure import from src/main ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))      # .../mangage_clubs/src
MAIN_DIR = os.path.join(BASE_DIR, "main")                  # .../mangage_clubs/src/main

if MAIN_DIR not in sys.path:
    sys.path.insert(0, MAIN_DIR)

from club_system import ClubSystem


@pytest.fixture
def system():
    """Creates a fresh system with ACM as an existing club."""
    s = ClubSystem()
    s.existing_clubs.add("ACM")
    return s


# ---------------- BOUNDARY VALUE TESTS ----------------

def test_boundary_clubname_whitespace_only(system):
    result = system.create_club("   ", "a" * 50)
    assert result == "Club Name cannot be empty"


def test_boundary_description_len_49(system):
    result = system.create_club("New Club", "a" * 49)
    assert result == "Description must be at least 50 characters"


def test_boundary_description_len_50(system):
    result = system.create_club("New Club", "a" * 50)
    assert result == "Club Created Successfully"


def test_boundary_description_len_51(system):
    result = system.create_club("New Club 2", "a" * 51)
    assert result == "Club Created Successfully"


def test_boundary_description_whitespace_49(system):
    result = system.create_club("Whitespace49", " " * 49)
    assert result == "Description cannot be empty"


def test_boundary_description_whitespace_50(system):
    result = system.create_club("Whitespace50", " " * 50)
    assert result == "Description cannot be empty"


def test_boundary_description_valid_with_padding(system):
    desc = "   " + ("a" * 50) + "   "
    result = system.create_club("Padded Description", desc)
    assert result == "Club Created Successfully"
