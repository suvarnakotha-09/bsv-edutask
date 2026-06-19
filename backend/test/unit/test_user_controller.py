import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController


# TC1 - Valid email with a single matching user
def test_get_user_single_result():

    dao = Mock()
    dao.find.return_value = [
        {"email": "suvarna@test.com"}
    ]

    controller = UserController(dao)

    result = controller.get_user_by_email(
        "suvarna@test.com"
    )

    assert result == {
        "email": "suvarna@test.com"
    }


# TC2 - Valid email with multiple matching users
def test_get_user_multiple_results():

    dao = Mock()
    dao.find.return_value = [
        {"email": "suvarna@test.com"},
        {"email": "suvarna@test.com"}
    ]

    controller = UserController(dao)

    result = controller.get_user_by_email(
        "suvarna@test.com"
    )

    assert result == {
        "email": "suvarna@test.com"
    }


# TC3 - Valid email with no matching users
def test_get_user_no_results():

    dao = Mock()
    dao.find.return_value = []

    controller = UserController(dao)

    result = controller.get_user_by_email(
        "suvarna@test.com"
    )

    assert result is None


# TC4 - Invalid email format
def test_invalid_email():

    dao = Mock()

    controller = UserController(dao)

    with pytest.raises(ValueError):

        controller.get_user_by_email(
            "invalid-email"
        )


# TC5 - Empty email input
def test_empty_email():

    dao = Mock()

    controller = UserController(dao)

    with pytest.raises(ValueError):

        controller.get_user_by_email(
            ""
        )


# TC6 - DAO raises exception
def test_dao_exception():

    dao = Mock()
    dao.find.side_effect = Exception(
        "Database error"
    )

    controller = UserController(dao)

    with pytest.raises(Exception):

        controller.get_user_by_email(
            "suvarna@test.com"
        )
