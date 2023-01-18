import pytest
from app.core.common.base.exceptions import ValidationError
from app.core.user.entities.user import (
    Username,
    RawPassword,
    Email,
)


class TestEmail:
    def test_email_without_at(self):
        with pytest.raises(ValidationError):
            Email("testgmail.com")

    def test_email_with_spaces(self):
        with pytest.raises(ValidationError):
            Email("test @gmail.com")

    def test_email_without_username(self):
        with pytest.raises(ValidationError):
            Email("@gmail.com")

    def test_email_without_domain(self):
        with pytest.raises(ValidationError):
            Email("test@")

    def test_email_with_wrong_domain(self):
        with pytest.raises(ValidationError):
            Email("test@gmailcom")

    def test_email(self):
        Email("test@gmail.com")


class TestPassword:
    def test_password_without_digits(self):
        with pytest.raises(ValidationError):
            RawPassword("TestPassword!")

    def test_password_without_uppercase(self):
        with pytest.raises(ValidationError):
            RawPassword("testpassword1!")

    def test_password_without_lowercase(self):
        with pytest.raises(ValidationError):
            RawPassword("TESTPASSWORD1!")

    def test_password_without_special_characters(self):
        with pytest.raises(ValidationError):
            RawPassword("TestPassword1")

    def test_password_less_than_8_characters(self):
        with pytest.raises(ValidationError):
            RawPassword("Test1!")

    def test_password(self):
        RawPassword("TestPassword1!")


class TestUsername:

    def test_username_not_str(self):
        with pytest.raises(ValidationError):
            Username(123)

    def test_username_short(self):
        with pytest.raises(ValidationError):
            Username("te")

    def test_username_long(self):
        with pytest.raises(ValidationError):
            Username("testtesttesttesttesttesttesttesttest")

    def test_username_with_spaces(self):
        with pytest.raises(ValidationError):
            Username("test test")

    def test_username_start_digit(self):
        with pytest.raises(ValidationError):
            Username("1test")

    def test_username_special_characters(self):
        with pytest.raises(ValidationError):
            Username("test-test")

    def test_username_special_characters_2(self):
        with pytest.raises(ValidationError):
            Username("test@test")

    def test_username_with_digit(self):
        with pytest.raises(ValidationError):
            Username("1")
