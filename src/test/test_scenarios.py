# In test_scenarios.py
import pytest
from club_system import ClubSystem

@pytest.fixture
def system():
    """ Sets up a new system and pre-loads "ACM" as an existing club. """
    system = ClubSystem()
    system.existing_clubs.add("ACM")  # <--- THIS IS THE FIX. ADD THIS LINE.
    return system

# --- Concrete Scenario Test Cases ---

def test_case_1_valid_valid(system):
    # Test Case 1: (Valid, Valid)
    club_name = "HackUTD"
    description = "The official Student-Run Hackathon at UTD. We organize events, workshops, and a 24-hour hackathon for students to innovate."
    expected_result = "Club Created Successfully"
    
    assert system.create_club(club_name, description) == expected_result
    assert "HackUTD" in system.existing_clubs

def test_case_2_valid_invalid_desc_short(system):
    # Test Case 2: (Valid, Invalid)
    club_name = "UTDAI"
    description = "A club for AI."
    expected_result = "Description must be at least 50 characters"
    
    assert system.create_club(club_name, description) == expected_result

def test_case_3_valid_exceptional_desc_empty(system):
    # Test Case 3: (Valid, Exceptional)
    club_name = "Women in CS"
    description = ""
    expected_result = "Description cannot be empty"
    
    assert system.create_club(club_name, description) == expected_result

def test_case_4_invalid_name_exists_valid_desc(system):
    # Test Case 4: (Invalid, Valid)
    club_name = "ACM"  # Exists (from fixture)
    description = "The Association for Computing Machinery. We aim to foster a strong community for computer science students through events and resources."
    expected_result = "A club with this name already exists"
    
    assert system.create_club(club_name, description) == expected_result

def test_case_5_invalid_name_exists_invalid_desc(system):
    # Test Case 5: (Invalid, Invalid)
    club_name = "ACM"
    description = "Another CS club."
    expected_result = "A club with this name already exists"
    
    assert system.create_club(club_name, description) == expected_result

def test_case_6_invalid_name_exists_exceptional_desc(system):
    # Test Case 6: (Invalid, Exceptional)
    club_name = "ACM"
    description = ""
    expected_result = "A club with this name already exists"
    
    assert system.create_club(club_name, description) == expected_result

def test_case_7_exceptional_name_empty_valid_desc(system):
    # Test Case 7: (Exceptional, Valid)
    club_name = ""
    description = "A new club for students interested in competitive video gaming and e-sports tournaments on campus."
    expected_result = "Club Name cannot be empty"
    
    assert system.create_club(club_name, description) == expected_result

def test_case_8_exceptional_name_empty_invalid_desc(system):
    # Test Case 8: (Exceptional, Invalid)
    club_name = ""
    description = "e-sports"
    expected_result = "Club Name cannot be empty"
    
    assert system.create_club(club_name, description) == expected_result

def test_case_9_exceptional_name_empty_exceptional_desc_empty(system):
    # Test Case 9: (Exceptional, Exceptional)
    club_name = ""
    description = ""
    expected_result = "Club Name cannot be empty"
    
    assert system.create_club(club_name, description) == expected_result
