import bcrypt

from db import students, users


def hash_password(plain_password):
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())


def verify_password(plain_password, password_hash):
    return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash)


def default_password(student):
    return student["date_of_birth"].strftime("%d%m%Y")


def authenticate(roll_number, password):
    user = users.find_one({"roll_number": roll_number})
    if user is None:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return students.find_one({"roll_number": roll_number}, {"_id": 0})

MIN_PASSWORD_LENGTH = 8


def change_password(roll_number, current_password, new_password):
    user = users.find_one({"roll_number": roll_number})
    if user is None or not verify_password(current_password, user["password_hash"]):
        return False, "Current password is incorrect"

    if len(new_password) < MIN_PASSWORD_LENGTH:
        return False, f"New password must be at least {MIN_PASSWORD_LENGTH} characters"

    if new_password == current_password:
        return False, "New password must be different from the current one"

    users.update_one(
        {"roll_number": roll_number},
        {"$set": {"password_hash": hash_password(new_password)}},
    )
    return True, "Password changed successfully"