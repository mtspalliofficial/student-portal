import argparse
import json
import random
from datetime import date
from pathlib import Path

from faker import Faker
from db import check_connection, init_indexes
from importer import import_students

fake = Faker("en_IN")

DEPARTMENTS = {
    "CSE": "B.Tech",
    "ECE": "B.Tech",
    "EEE": "B.Tech",
    "MECH": "B.Tech",
    "CS": "B.Sc",
}

SUBJECTS = {
    "CSE": ["Data Structures", "Operating Systems", "Computer Networks", "Database Systems",
            "Algorithms", "Software Engineering", "Machine Learning", "Compiler Design",
            "Web Technologies", "Discrete Mathematics"],
    "ECE": ["Signals and Systems", "Digital Electronics", "Analog Circuits", "Electromagnetics",
            "Microprocessors", "Communication Systems", "VLSI Design", "Control Systems",
            "Embedded Systems", "Network Theory"],
    "EEE": ["Electrical Machines", "Power Systems", "Circuit Theory", "Power Electronics",
            "Control Systems", "Measurements", "Electric Drives", "High Voltage Engineering",
            "Renewable Energy", "Digital Electronics"],
    "MECH": ["Thermodynamics", "Fluid Mechanics", "Strength of Materials", "Machine Design",
             "Manufacturing Processes", "Heat Transfer", "Kinematics", "CAD/CAM",
             "Engineering Mechanics", "IC Engines"],
    "CS": ["Programming in C", "Data Structures", "Database Systems", "Python Programming",
           "Computer Networks", "Operating Systems", "Web Development", "Statistics",
           "Java Programming", "Discrete Mathematics"],
}
SUBJECTS_PER_SEMESTER = 5

GRADE_SCALE = [
    (90, "O", 10),
    (80, "A+", 9),
    (70, "A", 8),
    (60, "B+", 7),
    (50, "B", 6),
    (40, "C", 5),
    (0, "F", 0),
]

def grade_for(marks):
    for minimum, grade, points in GRADE_SCALE:
        if marks >= minimum:
            return grade, points


def generate_marks(department, completed_semesters):
    ability = random.uniform(50, 92)
    semesters = []
    for semester in range(1, completed_semesters + 1):
        subjects = []
        for name in random.sample(SUBJECTS[department], SUBJECTS_PER_SEMESTER):
            marks = max(0, min(100, round(random.gauss(ability, 8))))
            grade, points = grade_for(marks)
            subjects.append({"subject": name, "marks": marks, "grade": grade, "points": points})
        sgpa = round(sum(subject["points"] for subject in subjects) / len(subjects), 2)
        semesters.append({"semester": semester, "subjects": subjects, "sgpa": sgpa})
    return semesters

def generate_student(seq):
    gender = random.choice(["Male", "Female"])
    if gender == "Male":
        first_name = fake.first_name_male()
    else:
        first_name = fake.first_name_female()
    last_name = fake.last_name()

    department = random.choice(list(DEPARTMENTS))
    admission_year = random.randint(2022, 2025)
    roll_number = f"{department}{admission_year}{seq:03d}"

    years_studied = date.today().year - admission_year
    semester = min(years_studied * 2 + 1, 8)
    marks = generate_marks(department, semester - 1)

    dob = fake.date_of_birth(minimum_age=18, maximum_age=24)

    return {
        "roll_number": roll_number,
        "name": f"{first_name} {last_name}",
        "email": f"{first_name.lower()}.{last_name.lower()}{seq}@college.edu",
        "phone": f"{random.choice('6789')}{random.randint(0, 999999999):09d}",
        "date_of_birth": dob.isoformat(),
        "gender": gender,
        "department": department,
        "course": DEPARTMENTS[department],
        "semester": semester,
        "admission_year": admission_year,
        "address": {"city": fake.city(), "state": fake.state()},
        "cgpa": round(sum(record["sgpa"] for record in marks) / len(marks), 2) if marks else None,
        "marks": marks,
    }

def main():
    parser = argparse.ArgumentParser(description="Generate fake student data as JSON")
    parser.add_argument("--count", type=int, default=50, help="Number of students to generate")
    parser.add_argument("--output", default="data/students.json", help="Output JSON file path")
    parser.add_argument("--seed", type=int, help="Seed for repeatable data")
    parser.add_argument("--import-db", action="store_true", help="Import the generated data into MongoDB")
    args = parser.parse_args()

    if args.count < 1:
        parser.error("--count must be at least 1")

    if args.seed is not None:
        random.seed(args.seed)
        Faker.seed(args.seed)

    students = [generate_student(i) for i in range(1, args.count + 1)]

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2)

    print(f"Generated {len(students)} students -> {output_path}")

    if args.import_db:
        check_connection()
        init_indexes()
        import_students(output_path)

if __name__ == "__main__":
    main()