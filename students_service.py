import re

from pymongo import ReturnDocument

from db import students, marks

PHONE_PATTERN = re.compile(r"^[6-9]\d{9}$")
EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.]+$")


def update_contact_details(roll_number, phone, email, city, state):
    if not PHONE_PATTERN.match(phone):
        return False, "Phone must be 10 digits starting with 6, 7, 8 or 9", None

    if not EMAIL_PATTERN.match(email):
        return False, "Please enter a valid email address", None

    if not city or not state:
        return False, "City and state cannot be empty", None

    updated_student = students.find_one_and_update(
        {"roll_number": roll_number},
        {"$set": {
            "phone": phone,
            "email": email,
            "address.city": city,
            "address.state": state,
        }},
        projection={"_id": 0},
        return_document=ReturnDocument.AFTER,
    )

    if updated_student is None:
        return False, "Student not found", None
    return True, "Profile updated successfully", updated_student

def get_marks(roll_number):
    return list(marks.find({"roll_number": roll_number}, {"_id": 0}).sort("semester", 1))