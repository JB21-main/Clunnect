import os
import sys
import pytest

# --- Make sure from import club_system.py from src/main ---
BASE_DIR = os.path.dirname(os.path.dirname(__file__))      # .../mangage_clubs/src
MAIN_DIR = os.path.join(BASE_DIR, "main")                  # .../mangage_clubs/src/main

if MAIN_DIR not in sys.path:
    sys.path.insert(0, MAIN_DIR)

from club_system import ClubSystem


@pytest.fixture
def system():
    """Sets up a new system and pre-loads 'ACM' as an existing club."""
    s = ClubSystem()
    # Preload ACM as an existing club with a valid description
    valid_desc = "A" * 60
    s.existing_clubs.add("ACM")
    s.clubs["ACM"] = valid_desc
    return s


# ---------- Boundary tests for create_club ----------

def test_name_boundary_whitespace_only(system):
    """Club name is only spaces → treated as empty."""
    result = system.create_club("   ", "a" * 50)
    assert result == "Club Name cannot be empty"


def test_description_boundary_len_49(system):
    """Description just below minimum length (49)."""
    result = system.create_club("New Club", "a" * 49)
    assert result == "Description must be at least 50 characters"


def test_description_boundary_len_50(system):
    """Description exactly at minimum length (50)."""
    result = system.create_club("New Club", "a" * 50)
    assert result == "Club Created Successfully"


def test_description_boundary_len_51(system):
    """Description just above minimum length (51)."""
    result = system.create_club("New Club 2", "a" * 51)
    assert result == "Club Created Successfully"


def test_description_boundary_whitespace_len_49(system):
    """49 whitespace chars → considered empty after strip()."""
    result = system.create_club("New Club", " " * 49)
    assert result == "Description cannot be empty"


def test_description_boundary_whitespace_len_50(system):
    """50 whitespace chars → considered empty after strip()."""
    result = system.create_club("New Club", " " * 50)
    assert result == "Description cannot be empty"


def test_description_boundary_with_leading_whitespace(system):
    """Valid description with leading & trailing spaces still passes."""
    desc = "   " + ("a" * 50) + "   "  # 56 chars total, 50 non-space
    result = system.create_club("Whitespace Club", desc)
    assert result == "Club Created Successfully"


# ---------- New boundary tests for update_club & delete_club ----------

def test_update_boundary_nonexistent_club(system):
    """Updating a club that does not exist."""
    result = system.update_club("Nonexistent", "a" * 60)
    assert result == "Club not found"


def test_update_boundary_description_len_49(system):
    """Update existing club with too-short description."""
    result = system.update_club("ACM", "a" * 49)
    assert result == "Description must be at least 50 characters"


def test_update_boundary_valid_update(system):
    """Update existing club with valid description."""
    new_desc = "Updated description for ACM that is definitely long enough."
    result = system.update_club("ACM", new_desc)
    assert result == "Club Updated Successfully"
    assert system.clubs["ACM"] == new_desc


def test_delete_boundary_nonexistent_club(system):
    """Deleting a non-existing club."""
    result = system.delete_club("Nonexistent")
    assert result == "Club not found"


def test_delete_boundary_existing_club(system):
    """Deleting an existing club removes it from storage."""
    result = system.delete_club("ACM")
    assert result == "Club Deleted Successfully"
    assert "ACM" not in system.existing_clubs
    assert "ACM" not in system.clubs
