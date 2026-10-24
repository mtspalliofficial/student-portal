# Student Portal (Python + MongoDB)

A desktop student portal built entirely in Python. Students sign in with their roll number and see their personal details, academic summary and semester-wise marks, and can update their contact details and password. The project also includes a command-line tool that generates realistic student data and imports it into MongoDB in a single command.

## Features

- **Secure login**: passwords are stored only as bcrypt hashes, never in plain text
- **Dashboard**: CGPA, current semester, admission year, personal and contact details
- **Marks**: semester-wise subject marks, grades (10-point scale) and SGPA
- **Edit Profile**: update phone, email and address with regex-based validation
- **Change Password**: verifies the current password and enforces password rules
- **Light/Dark theme** toggle and a sidebar-based multi-page layout
- **Data generator**: realistic Indian student data with Faker (`en_IN` locale), with marks, grades and a CGPA calculated from SGPAs
- **Idempotent importer**: safe to run any number of times, with no duplicates (upserts + unique indexes)
- **One-command pipeline**: generate and import data with a single `--import-db` flag

## Tech Stack

| Area | Tools |
|---|---|
| Language | Python 3.11 |
| Database | MongoDB Community Server, pymongo |
| UI | CustomTkinter (built on Tkinter) |
| Security | bcrypt |
| Data generation | Faker |
| CLI and config | argparse, python-dotenv |

## Project Structure

```
student_portal/
├── main.py                 # App entry point; switches between login and portal
├── config.py               # Loads settings from .env
├── db.py                   # The only module that talks to MongoDB directly; indexes
├── auth.py                 # Password hashing, login check, change password
├── students_service.py     # Profile updates and marks queries
├── generator.py            # CLI tool: generates fake students and marks as JSON
├── importer.py             # CLI tool: validates the JSON and upserts it into MongoDB
├── requirements.txt
├── .env.example            # Template for your .env file
├── screenshots/
└── ui/
    ├── theme.py            # Shared colours and fonts (light and dark)
    ├── login_window.py     # Login screen
    ├── portal_window.py    # Portal shell: sidebar and page switching
    └── pages/
        ├── dashboard_page.py
        ├── marks_page.py
        ├── profile_page.py
        └── password_page.py
```

## Setup

**Prerequisites:** Python 3.10+ and [MongoDB Community Server](https://www.mongodb.com/try/download/community) running locally (MongoDB Compass is optional, for browsing the data).

```bash
git clone https://github.com/<your-username>/student-portal.git
cd student-portal

python -m venv .venv
.\.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate         # macOS / Linux

python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and adjust it if your MongoDB runs somewhere else:

```
MONGO_URI=mongodb://localhost:27017
DB_NAME=student_portal_db
```

## Usage

**1. Generate and import student data**

```bash
python generator.py --count 50 --seed 42 --import-db
```

| Option | Meaning |
|---|---|
| `--count` | Number of students to generate (default 50) |
| `--seed` | Makes the data reproducible: same seed, same students |
| `--output` | Output JSON path (default `data/students.json`) |
| `--import-db` | Import the generated file into MongoDB right away |

You can also import any JSON file separately:

```bash
python importer.py data/students.json
```

**2. Run the app**

```bash
python main.py
```

**3. Log in**

- **Roll number:** any `roll_number` from `data/students.json` (e.g. `CS2025001`)
- **Default password:** the student's date of birth as `DDMMYYYY` (e.g. `2004-11-11` → `11112004`)

## Design Decisions

- **Separate `users` and `students` collections.** Login data (password hashes) is kept apart from the profile data the UI displays, so a display bug can never leak a hash.
- **bcrypt for passwords.** Salted and deliberately slow, which makes stolen hashes expensive to crack. Login errors never reveal whether a roll number exists.
- **Idempotent imports.** Students are upserted by `roll_number` with `bulk_write` (one database round trip), and unique indexes enforce no duplicates at the database level.
- **Student edits survive re-imports.** Official fields use `$set`, while student-editable fields (phone, email, address) use `$setOnInsert`, so they're only written when a student is first created.
- **Marks in their own collection.** One document per student per semester, with a compound unique index on (`roll_number`, `semester`). This keeps student documents small and makes cross-student analysis straightforward.
- **Layered architecture.** UI → service modules (`auth.py`, `students_service.py`) → `db.py`. The UI never queries MongoDB directly, and validation and security rules live in the service layer.
- **Generator and importer are decoupled.** The generator only writes JSON; the importer validates and loads any JSON in the expected format, not just generated data.

## Screenshots

| Login | Dashboard |
|---|---|
| ![Login](screenshots/login.png) | ![Dashboard](screenshots/dashboard.png) |

## Future Improvements

- Admin dashboard with role-based access, student search and aggregation-based analytics
- Attendance tracking
- Export marks as a PDF report
- Automated tests with pytest

## Author

**Mokshajna Palli**
B.Tech CSE (AI & ML)