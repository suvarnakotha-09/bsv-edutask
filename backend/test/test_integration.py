import pytest
from pymongo.errors import WriteError


class TestUserCreationIntegration:

    def test_create_user_successfully(self, user_dao):

        user = {
            "firstName": "Suvarna",
            "lastName": "Devi",
            "email": "suvarna.kotha@student.com"
        }

        created_user = user_dao.create(user)

        assert created_user is not None
        assert "_id" in created_user
        assert created_user["email"] == "suvarna.kotha@student.com"

    def test_create_user_without_email(self, user_dao):

        user = {
            "firstName": "Suvarna",
            "lastName": "Devi"
        }

        with pytest.raises(WriteError):
            user_dao.create(user)

    def test_create_user_with_invalid_firstname_type(self, user_dao):

        user = {
            "firstName": False,
            "lastName": "Devi",
            "email": "suvarna.kotha@student.com"
        }

        with pytest.raises(WriteError):
            user_dao.create(user)

    def test_create_user_with_existing_email(self, user_dao):

        original_user = {
            "firstName": "Suvarna",
            "lastName": "Devi",
            "email": "duplicate@student.com"
        }

        duplicate_user = {
            "firstName": "Harika",
            "lastName": "Rani",
            "email": "duplicate@student.com"
        }

        user_dao.create(original_user)

        with pytest.raises(WriteError):
            user_dao.create(duplicate_user)