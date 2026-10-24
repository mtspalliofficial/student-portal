import argparse
import json
from datetime import datetime
from pathlib import Path

from pymongo import UpdateOne

from db import students, users, marks, check_connection, init_indexes
from auth import hash_password, default_password

REQUIRED_FIELDS = [
    "roll_number", "name", "email", "department",
    "course", "semester", "admission_year", "date_of_birth",
]
STUDENT_EDITABLE_FIELDS = ["phone", "email", "address"]


def load_students(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("JSON file must contain a list of students")
    return data


def prepare_student(raw):
    missing = [field for field in REQUIRED_FIELDS if field not in raw]
    if missing:
        raise ValueError(f"missing fields: {', '.join(missing)}")

    student = dict(raw)
    student["date_of_birth"] = datetime.strptime(raw["date_of_birth"], "%Y-%m-%d")
    semester_records = student.pop("marks", [])
    return student, semester_records


def import_students(file_path):
    raw_students = load_students(file_path)
    existing_users = set(users.distinct("roll_number"))

    student_operations = []
    mark_operations = []
    new_users = []
    skipped = 0

    for index, raw in enumerate(raw_students, start=1):
        try:
            student, semester_records = prepare_student(raw)
        except ValueError as error:
            print(f"Skipping record {index}: {error}")
            skipped += 1
            continue

        roll_number = student["roll_number"]

        always_update = {key: value for key, value in student.items() if key not in STUDENT_EDITABLE_FIELDS}
        only_on_insert = {key: value for key, value in student.items() if key in STUDENT_EDITABLE_FIELDS}

        student_operations.append(
            UpdateOne(
                {"roll_number": roll_number},
                {"$set": always_update, "$setOnInsert": only_on_insert},
                upsert=True,
            )
        )

        for record in semester_records:
            mark_operations.append(
                UpdateOne(
                    {"roll_number": roll_number, "semester": record["semester"]},
                    {"$set": {"subjects": record["subjects"], "sgpa": record["sgpa"]}},
                    upsert=True,
                )
            )

        if roll_number not in existing_users:
            new_users.append({
                "roll_number": roll_number,
                "password_hash": hash_password(default_password(student)),
                "role": "student",
            })

    if not student_operations:
        print("Nothing to import.")
        return

    result = students.bulk_write(student_operations)
    print(f"Inserted:  {result.upserted_count}")
    print(f"Updated:   {result.modified_count}")
    print(f"Unchanged: {result.matched_count - result.modified_count}")
    print(f"Skipped:   {skipped}")

    if mark_operations:
        marks.bulk_write(mark_operations)
    print(f"Marks:     {len(mark_operations)} semester records")

    if new_users:
        users.insert_many(new_users)
    print(f"Accounts:  {len(new_users)} created")


def main():
    parser = argparse.ArgumentParser(description="Import students from a JSON file into MongoDB.")
    parser.add_argument("file", nargs="?", default="data/students.json", help="Path to the JSON file")
    args = parser.parse_args()

    if not Path(args.file).exists():
        parser.error(f"File not found: {args.file}")

    check_connection()
    init_indexes()
    import_students(args.file)


if __name__ == "__main__":
    main()