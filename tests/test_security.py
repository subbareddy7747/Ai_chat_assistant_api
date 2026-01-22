from app.core.security import get_password_hash, verify_password


def test_hash_and_verify_password():
    password = "SecurePass123!"
    hashed = get_password_hash(password)

    # hash should not equal plaintext
    assert hashed != password

    # correct password should validate
    assert verify_password(password, hashed) is True


def test_verify_wrong_password():
    password = "SecurePass123!"
    hashed = get_password_hash(password)

    # wrong password should fail
    assert verify_password("WrongPassword!", hashed) is False
