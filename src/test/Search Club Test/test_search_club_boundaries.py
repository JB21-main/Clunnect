import pytest
from Services.DBmgr import DBmgr
from Controllers.SearchController import SearchController

@pytest.fixture
def system():
    dbMgr = DBmgr()
    sys = SearchController(dbMgr)
    return sys

def test_boundary_empty_search_query(system):
    """Empty search query — invalid input."""
    result = system.search("")
    assert result == []

def test_boundary_whitespace_search_query(system):
    """Whitespace search query — invalid input."""
    result = system.search("   ")
    assert result == []

def test_boundary_null(system):
    """Null search query — invalid input."""
    result = system.search(None)
    assert result == []

def test_boundary_successful_search(system):
    """Valid search query — valid boundary."""
    result = system.search("ACM")
    assert isinstance(result, list)

def test_boundary_unsuccessful_search(system):
    """Search query with no matching results — valid boundary."""
    result = system.search("NonExistentClubName")
    assert result == []