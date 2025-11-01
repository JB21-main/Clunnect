import pytest
from club_system import ClubSystem

@pytest.fixture
def system():
    """ Sets up a new system and pre-loads "ACM" as an existing club. """
    system = ClubSystem() 
    system.existing_clubs.add("ACM")
    return system

# --- Boundary Value Test Cases ---

def test_name_boundary_whitespace_only(system):
    """ Tests a club name that consists only of spaces. """
    club_name = "   "
    description = "a" * 50  # Valid description
    expected = "Club Name cannot be empty"
    
    assert system.create_club(club_name, description) == expected

def test_description_boundary_len_49(system):
    """ Tests a description that is just *below* the minimum length. """
    club_name = "New Club"
    description = "a" * 49  # 49 characters
    expected = "Description must be at least 50 characters"
    
    assert system.create_club(club_name, description) == expected

def test_description_boundary_len_50(system):
    """ Tests a description that is exactly *at* the minimum length. """
    club_name = "New Club"
    description = "a" * 50  # 50 characters
    expected = "Club Created Successfully"
    
    assert system.create_club(club_name, description) == expected

def test_description_boundary_len_51(system):
    """ Tests a description that is just *above* the minimum length. """
    club_name = "New Club 2"
    description = "a" * 51  # 51 characters
    expected = "Club Created Successfully"
    
    assert system.create_club(club_name, description) == expected

def test_description_boundary_whitespace_len_49(system):
    """ Tests a description of 49 whitespace chars. Should fail the 'empty' check. """
    club_name = "New Club"
    description = " " * 49
    expected = "Description cannot be empty"
    
    # This should fail the 'club_description.strip() == ""' check
    assert system.create_club(club_name, description) == expected

def test_description_boundary_whitespace_len_50(system):
    """ Tests a description of 50 whitespace chars. Should fail the 'empty' check. """
    club_name = "New Club"
    description = " " * 50
    expected = "Description cannot be empty"
    
    # This should also fail the 'club_description.strip() == ""' check
    assert system.create_club(club_name, description) == expected

def test_description_boundary_with_leading_whitespace(system):
    """ Tests a valid description that has leading/trailing whitespace. """
    club_name = "Whitespace Club"
    description = "   " + ("a" * 50) + "   "  # Length 56, but 50 after strip
    expected = "Club Created Successfully"
    
    assert system.create_club(club_name, description) == expected
