import pytest
from Services.DBmgr import DBmgr
from Controllers.AuthController import AuthController

@pytest.fixture
def controller():
    db_mgr = DBmgr()
    auth_controller = AuthController(db_mgr)
    return auth_controller

# Successful authorization
def test_boundary_successful_auth(controller):
    result, message = controller.authenticate("txs201100@utdallas.edu", "TestUser1234")
    assert result == True

# Wrong password
def test_boundary_wrong_password(controller):
    result, message = controller.authenticate("txs201100@utdallas.edu", "WrongPassword")
    assert result == False
    assert message == "Incorrect password"

def test_boundary_empty_username(controller):
    result, message = controller.authenticate("", "TestUser1234")
    assert result == False
    assert message == "Invalid email format"

def test_boundary_empty_password(controller):
    result, message = controller.authenticate("txs201100@utdallas.edu", "");
    assert result == False
    assert message == "Incorrect password"

def test_boundary_invalid_user(controller):
    result, message = controller.authenticate("tsx201100@utdalls.edu", "TestUser1234")
    assert result == False
    assert message == "An account with that email was not found"

def test_boundary_both_blank(controller):
    result, message = controller.authenticate("", "")
    assert result == False
    assert message == "Invalid email format"