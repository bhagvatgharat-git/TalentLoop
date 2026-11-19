# TalentLoop - Recruitment & Placement Management System

Subtitle: Recruitment & Placement System  
Tagline: "From application to joining, in one loop."

## Overview
TalentLoop is a console-based recruitment and placement management application built in Python and MySQL. It was developed as an internship project to handle the complete campus recruitment cycle, from student registration and job postings to eligibility screening, multi-round interviews, offer letters, and confirmed student joinings.

## The Problem It Solves
Placement cells in colleges and training institutes frequently manage campus recruitment using spreadsheets, chat groups, and shared folders. This informal process leads to several practical issues:
- Students applying for roles for which they do not meet academic criteria (percentage, passing year, or active backlogs).
- Difficulty tracking what stage each student is currently at across multiple hiring drives.
- Accidental duplicate applications or duplicate offers.
- No central record of interview rounds, reviewer remarks, and ratings.
- Inaccurate counts of remaining job openings as candidates accept offers.

TalentLoop brings all of these stages into a structured relational system with strict validation rules, so an applicant cannot skip stages or bypass eligibility criteria.

## The Workflow and Meaning of the Name
The name **TalentLoop** represents closing the loop on talent acquisition: rather than treating applications, interviews, and final placements as disconnected steps, the application tracks candidates through a continuous, closed lifecycle:

```
[ APPLIED ] 
     |
     v
[ SHORTLISTED ] 
     |
     v
[ INTERVIEW ] 
     |
     v
[ SELECTED ] 
     |
     v
[ OFFERED ] 
     |
     v
[ JOINED ]
```

At any stage before reaching `JOINED`, an application can transition to `REJECTED` (for instance, failing an interview round, candidate declining an offer, or administrative screening). Once an application reaches `JOINED` or `REJECTED`, it is terminal and cannot jump backward.

## Tech Stack
- Programming Language: Python 3.12+
- Database: MySQL 8.0+
- Database Driver: `mysql-connector-python` (version pinned in requirements.txt)
- User Interface: Command-line interface (Console menu only, no web frameworks)
- Testing: Python `unittest` framework with `unittest.mock`

## Architecture
The application follows a strict layered architecture:

```
Main Menu (rpms/app)
       |
       v
Business Logic & Validation (rpms/service)
       |
       v
Data Access Objects (rpms/dao)
       |
       v
MySQL Connector
       |
       v
MySQL Database (talentloop_db)
```

Layer responsibilities:
- `rpms/app`: Presents menus, collects user input, re-prompts on invalid inputs, and displays aligned tables.
- `rpms/service`: Enforces domain rules, eligibility evaluations, status transitions, and activity logging.
- `rpms/dao`: Executes parameterized SQL statements (`%s`) and maps query rows to model objects.
- `rpms/model`: Plain Python data structures with `__init__` and `__str__` containing no business logic or database queries.
- `rpms/util`: Helper utilities including database connection providers, validators, ID generators, loggers, and tabular printers.
- `rpms/exception`: Domain-specific exception hierarchy rooted at `RPMSException`.

## Folder Structure
```
TalentLoop/
├── docs/
│   └── test_cases.md
├── rpms/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── application_menu.py
│   │   ├── candidate_menu.py
│   │   ├── company_menu.py
│   │   ├── interview_menu.py
│   │   ├── job_menu.py
│   │   ├── main_menu.py
│   │   ├── offer_menu.py
│   │   ├── placement_menu.py
│   │   └── report_menu.py
│   ├── dao/
│   │   ├── __init__.py
│   │   ├── application_dao.py
│   │   ├── candidate_dao.py
│   │   ├── company_dao.py
│   │   ├── interview_dao.py
│   │   ├── job_dao.py
│   │   ├── offer_dao.py
│   │   ├── placement_dao.py
│   │   └── report_dao.py
│   ├── exception/
│   │   ├── __init__.py
│   │   └── custom_exceptions.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── application.py
│   │   ├── candidate.py
│   │   ├── company.py
│   │   ├── interview.py
│   │   ├── interview_feedback.py
│   │   ├── job.py
│   │   ├── offer.py
│   │   ├── placement.py
│   │   └── status.py
│   ├── service/
│   │   ├── __init__.py
│   │   ├── application_service.py
│   │   ├── candidate_service.py
│   │   ├── company_service.py
│   │   ├── eligibility_service.py
│   │   ├── interview_service.py
│   │   ├── job_service.py
│   │   ├── offer_service.py
│   │   ├── placement_service.py
│   │   └── report_service.py
│   ├── util/
│   │   ├── __init__.py
│   │   ├── branding.py
│   │   ├── config.py
│   │   ├── db_connection.py
│   │   ├── id_generator.py
│   │   ├── logger.py
│   │   ├── table_printer.py
│   │   └── validators.py
│   └── __init__.py
├── sql/
│   ├── sample_data.sql
│   └── schema.sql
├── tests/
│   ├── __init__.py
│   ├── test_candidate_service.py
│   ├── test_eligibility_and_application.py
│   └── test_offer_and_placement_service.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Setup Steps

### 1. Prerequisites
- Python 3.10 or higher installed.
- MySQL Server 8.0 or higher installed and running.

### 2. Database Setup
Open a terminal in the project root directory and run the database setup scripts using the MySQL client:

On Windows (PowerShell):
```powershell
Get-Content sql/schema.sql | mysql -u root -p
Get-Content sql/sample_data.sql | mysql -u root -p
```

On Linux or macOS (Bash):
```bash
mysql -u root -p < sql/schema.sql
mysql -u root -p < sql/sample_data.sql
```

This creates the `talentloop_db` database and populates it with realistic Indian sample data (14 candidates, 6 companies, 9 job postings, and consistent application and interview records).

### 3. Environment Configuration
The database parameters default to:
- `DB_HOST`: `localhost`
- `DB_USER`: `root`
- `DB_PASSWORD`: (empty string)
- `DB_NAME`: `talentloop_db`

To override these, set environment variables in your terminal before running the application:

On Windows PowerShell:
```powershell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="talentloop_db"
```

On Linux or macOS:
```bash
export DB_HOST="localhost"
export DB_USER="root"
export DB_PASSWORD="your_password"
export DB_NAME="talentloop_db"
```

### 4. Install Dependencies
Install the pinned MySQL connector:
```bash
pip install -r requirements.txt
```

### 5. Run the Application
Launch the console interface:
```bash
python main.py
```

### 6. Run the Test Suite
Run all unit tests using Python's standard test runner:
```bash
python -m unittest discover -s tests
```

## Modules

1. **Candidate Management**:
   - Add new candidates with automated ID generation (`CAN1001` format).
   - Validate 10-digit Indian mobile numbers (starting 6-9), email format, percentage (0-100), and non-negative backlogs.
   - Prevent duplicate email and mobile numbers.
   - Search by name or technology, view all (active/all), update details, or deactivate candidates.

2. **Company Management**:
   - Register hiring partners with unique company names, industry, location, contact person, and contact email.
   - Search by name, industry, or city.
   - Update company details with duplicate name verification.

3. **Job Management**:
   - Post job vacancies linked to registered companies.
   - Specify required technology, openings, package in LPA, minimum percentage, target passing year, maximum allowed backlogs, and future application deadline.
   - View open jobs with company name displayed via SQL JOIN.
   - Close active job postings.

4. **Eligibility & Applications**:
   - Check candidate qualification against any open job before applying.
   - Apply for jobs with automated validation.
   - Shortlist candidates, progress application stages, or reject candidates.
   - Filter applications by job, candidate, or status with candidate and job names resolved through SQL joins.

5. **Interview Management**:
   - Schedule interview rounds (round number, date, mode: Online/Offline, interviewer name).
   - Enforce that interviews can only be scheduled for applications in `SHORTLISTED` or `INTERVIEW` status.
   - Scheduling round 1 automatically advances a `SHORTLISTED` application to `INTERVIEW`.
   - Update interview status (`SCHEDULED`, `COMPLETED`, `CANCELLED`).
   - Record feedback (technical rating 1-10, communication rating 1-10, remarks, result: PASS/FAIL).
   - A `FAIL` result automatically moves the application to `REJECTED`.
   - A `PASS` result on a designated final round moves the application to `SELECTED`.

6. **Offer Management**:
   - Create offer letters strictly for applications in `SELECTED` status.
   - Specify designation, offered package in LPA, offer date, and joining date (must be strictly after the offer date).
   - Issuing an offer transitions the application to `OFFERED` in a database transaction.
   - Accepting or declining offers; a declined offer transitions the application to `REJECTED`.

7. **Placement Management**:
   - Record confirmed student placements strictly for `OFFERED` applications whose offer status is `ACCEPTED`.
   - Executes inside a database transaction:
     - Saves placement record.
     - Transitions application to `JOINED`.
     - Decrements the job opening count by 1.
     - Automatically closes the job when remaining openings reach zero.
   - Prevents duplicate placements for the same application.

8. **Analytics & Reports**:
   - Candidates by Technology (grouped count).
   - Open Jobs and Vacancies.
   - Applications by Workflow Status.
   - Company-wise Placements (total placed, average package, peak package).
   - Placed Candidates List (with package and joining dates).
   - Unplaced Active Candidates List (students with no `JOINED` application).

## Eligibility Rules
When evaluating whether a candidate can apply for a job, TalentLoop checks seven criteria in this exact sequential order:
1. **Candidate is active**: Inactive candidate profiles are barred from applying.
2. **Job is open**: The vacancy status must be `OPEN`.
3. **Deadline has not passed**: The job application deadline must be today or in the future.
4. **Candidate has not already applied**: Duplicate applications for the same job are blocked.
5. **Academic percentage**: The candidate's percentage must be greater than or equal to the job's minimum percentage.
6. **Passing year**: The candidate's passing year must match the job's target passing year.
7. **Backlog count**: The candidate's active backlogs must be less than or equal to the job's allowed maximum backlogs.

Evaluation halts at the first failed rule and reports the specific reason.

## Sample Console Usage

### Main Menu
```
==================================
TALENTLOOP
Recruitment & Placement System
==================================
1. Candidates
2. Companies
3. Jobs
4. Applications
5. Interviews
6. Offers
7. Placements
8. Reports
9. Exit

Enter choice (1-9): 1
```

### Candidate Table Output
```
ID      | Name         | Email                  | Mobile     | Technology   | Percentage | Year | Backlogs | Status
--------+--------------+------------------------+------------+--------------+------------+------+----------+-------
CAN1001 | Aarav Sharma | aarav.sharma@gmail.com | 9820011001 | Java         | 78.50%     | 2024 | 0        | Active
CAN1002 | Priya Patel  | priya.patel@gmail.com  | 9820011002 | Python       | 82.00%     | 2024 | 0        | Active
CAN1006 | Neha Joshi   | neha.joshi@gmail.com   | 9820011006 | Data Science | 88.60%     | 2024 | 0        | Active
--------+--------------+------------------------+------------+--------------+------------+------+----------+-------
Total records: 3
```

### Checking Candidate Eligibility
```
--- Check Candidate Eligibility ---
Enter Candidate ID (e.g. CAN1001): CAN1001
Enter Job ID (e.g. JOB101): JOB101

Eligibility Result:
Status: ELIGIBLE
Reason: Candidate meets all eligibility criteria.
```

### Company-wise Placements Report
```
Company ID | Company Name               | Placements | Avg Package (LPA) | Highest Package (LPA)
-----------+----------------------------+------------+-------------------+----------------------
COM101     | Tata Consultancy Services  | 1          | 4.50              | 4.50
COM103     | Persistent Systems         | 1          | 5.50              | 5.50
COM102     | Infosys Limited            | 0          | 0.00              | 0.00
COM104     | Wipro Technologies         | 0          | 0.00              | 0.00
COM105     | Zensar Technologies        | 0          | 0.00              | 0.00
COM106     | Cognizant Technology Sol.  | 0          | 0.00              | 0.00
-----------+----------------------------+------------+-------------------+----------------------
TOTAL      | 6 Companies                | 2          | 5.00              | 5.50
-----------+----------------------------+------------+-------------------+----------------------
Total records: 7
```

## Known Limitations and Future Improvements
- **Console Input Only**: The project is intentionally built as a console application for simplicity and focus on data modeling and layered architecture. A web API or UI was excluded by design.
- **Single Admin Session**: The system runs as a single administrative console without role-based login separation (e.g., separate student or recruiter logins). Adding role-based authentication would be a natural next step.
- **Notification Simulation**: Offers and interview invitations are recorded in the database and logged to `activity_log.txt`, but real-world email or SMS delivery is not integrated.
- **Batch Resumes**: Resumes and documents are not stored on the filesystem; candidate profiles rely on structured fields and technology tags.
- **Connection Pooling**: Currently, connections are created and closed per request/transaction. Under higher concurrency, a database connection pool would improve efficiency.
