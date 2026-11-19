# TalentLoop - Test Cases

| Attribute | Details |
| :--- | :--- |
| **Project** | TalentLoop (Recruitment & Placement Management System) |
| **Modules** | Candidates, Companies, Jobs, Eligibility & Applications, Interviews, Offers, Placements, Reports |
| **Tester** | |
| **Date** | 2026-11-20 |

---

### Test Execution Matrix

| Test ID | Module | Scenario | Input | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC-CAN-01 | Candidates | Register new candidate with valid details | Name: "Aarav Sharma", Email: "aarav.sharma@gmail.com", Mobile: "9820011001", Tech: "Java", %: 78.50, Year: 2024, Backlogs: 0 | Candidate registered with ID CAN1001, is_active=1 | As expected; candidate record created | PASS |
| TC-CAN-02 | Candidates | Block registration with duplicate email | Email: "aarav.sharma@gmail.com" (existing in DB) | Raise ValidationError: "A candidate with this email already exists" | ValidationError raised; duplicate blocked | PASS |
| TC-CAN-03 | Candidates | Block registration with duplicate mobile | Mobile: "9820011001" (existing in DB) | Raise ValidationError: "A candidate with this mobile number already exists" | ValidationError raised; duplicate blocked | PASS |
| TC-CAN-04 | Candidates | Validate academic percentage below minimum | Percentage: -5.0 | Raise ValidationError: "Percentage must be between 0.0 and 100.0" | ValidationError raised; negative rejected | PASS |
| TC-CAN-05 | Candidates | Validate academic percentage above maximum | Percentage: 105.0 | Raise ValidationError: "Percentage must be between 0.0 and 100.0" | ValidationError raised; excess rejected | PASS |
| TC-CAN-06 | Candidates | Validate negative backlog count | Backlog count: -1 | Raise ValidationError: "Backlog count must be a non-negative integer" | ValidationError raised; negative rejected | PASS |
| TC-COM-01 | Companies | Add new company with valid details | Name: "Tata Consultancy Services", Industry: "IT Services", Location: "Pune", Person: "Rajesh Kulkarni", Email: "rajesh.k@tcs.com" | Company created with ID COM101 | As expected; company created | PASS |
| TC-COM-02 | Companies | Block company registration with duplicate name | Name: "Tata Consultancy Services" (existing) | Raise ValidationError: "A company named ... already exists" | ValidationError raised; duplicate rejected | PASS |
| TC-COM-03 | Companies | Validate invalid contact email format | Contact email: "invalid-email-format" | Raise ValidationError: "Invalid email address" | ValidationError raised; invalid email rejected | PASS |
| TC-JOB-01 | Jobs | Post new job opening for valid company | Company: "COM101", Title: "Java Developer", Tech: "Java", Openings: 5, LPA: 4.50, Min%: 65.0, Year: 2024, MaxBacklogs: 0, Deadline: 2026-12-31 | Job created with ID JOB101 and status OPEN | As expected; job created | PASS |
| TC-JOB-02 | Jobs | Block job posting for non-existent company | Company ID: "COM999" | Raise CompanyNotFoundError | CompanyNotFoundError raised | PASS |
| TC-JOB-03 | Jobs | Block job posting with past application deadline | Deadline: 2020-01-01 (in the past) | Raise ValidationError: "Deadline must be today or a future date" | ValidationError raised; past date rejected | PASS |
| TC-JOB-04 | Jobs | Block job posting with zero or negative openings | Openings: 0 | Raise ValidationError: "Openings count must be a positive integer" | ValidationError raised; zero openings rejected | PASS |
| TC-ELIG-01 | Eligibility | Rule 1: Inactive candidate eligibility check | Candidate is_active = 0 | Return NOT ELIGIBLE: "Candidate ... is inactive" (Rule 1) | NOT ELIGIBLE returned; failed rule 1 | PASS |
| TC-ELIG-02 | Eligibility | Rule 2: Closed job opening eligibility check | Job status = "CLOSED" | Return NOT ELIGIBLE: "Job opening ... is closed" (Rule 2) | NOT ELIGIBLE returned; failed rule 2 | PASS |
| TC-ELIG-03 | Eligibility | Rule 3: Past job deadline eligibility check | Job deadline = past date | Return NOT ELIGIBLE: "Job application deadline has passed" (Rule 3) | NOT ELIGIBLE returned; failed rule 3 | PASS |
| TC-ELIG-04 | Eligibility | Rule 4: Candidate already applied check | Candidate CAN1001 already applied to JOB101 | Return NOT ELIGIBLE: "Candidate has already applied" (Rule 4) | NOT ELIGIBLE returned; failed rule 4 | PASS |
| TC-ELIG-05 | Eligibility | Rule 5: Candidate percentage below job minimum | Candidate%: 60.0, Job Min%: 65.0 | Return NOT ELIGIBLE: "Candidate percentage is below required minimum" (Rule 5) | NOT ELIGIBLE returned; failed rule 5 | PASS |
| TC-ELIG-06 | Eligibility | Rule 6: Passing year mismatch check | Candidate Year: 2023, Job Year: 2024 | Return NOT ELIGIBLE: "Candidate passing year does not match required year" (Rule 6) | NOT ELIGIBLE returned; failed rule 6 | PASS |
| TC-ELIG-07 | Eligibility | Rule 7: Excessive candidate backlogs check | Candidate Backlogs: 2, Job Max Backlogs: 0 | Return NOT ELIGIBLE: "Candidate backlog count exceeds allowed maximum" (Rule 7) | NOT ELIGIBLE returned; failed rule 7 | PASS |
| TC-ELIG-08 | Eligibility | Full eligibility pass | All 7 criteria satisfied | Return ELIGIBLE: "Candidate meets all eligibility criteria" | ELIGIBLE returned; all rules satisfied | PASS |
| TC-APP-01 | Applications | Submit application when duplicate exists | Re-applying with CAN1001 for JOB101 | Raise DuplicateApplicationError | DuplicateApplicationError raised | PASS |
| TC-APP-02 | Applications | Submit application when candidate not eligible | Ineligible candidate applies for JOB101 | Raise CandidateNotEligibleError with reason | CandidateNotEligibleError raised | PASS |
| TC-APP-03 | Applications | Sequential workflow transition | APPLIED -> SHORTLISTED -> INTERVIEW | Application transitions cleanly across valid states | Status updated to SHORTLISTED and INTERVIEW | PASS |
| TC-APP-04 | Applications | Block invalid workflow jump | APPLIED -> JOINED | Raise InvalidStatusTransitionError naming both states | InvalidStatusTransitionError raised | PASS |
| TC-INT-01 | Interviews | Schedule interview round 1 | App in SHORTLISTED status, Date: future, Mode: "Online" | Interview scheduled (INT101) and application moves to INTERVIEW | Interview scheduled; app status updated | PASS |
| TC-INT-02 | Interviews | Block interview scheduling for APPLIED state | Application status is APPLIED | Raise ValidationError: only allowed for SHORTLISTED or INTERVIEW | ValidationError raised; scheduling blocked | PASS |
| TC-INT-03 | Interviews | Record interview feedback with FAIL result | Result: "FAIL", Tech: 4, Comm: 5 | Feedback saved and application transitioned to REJECTED | Feedback saved; application marked REJECTED | PASS |
| TC-INT-04 | Interviews | Record final round interview feedback with PASS | Result: "PASS", is_final_round: True | Feedback saved and application transitioned to SELECTED | Feedback saved; application marked SELECTED | PASS |
| TC-OFF-01 | Offers | Create job offer for SELECTED application | Application in SELECTED status, LPA: 4.5, Joining > Offer Date | Offer created (OFF101) and application moves to OFFERED in single transaction | Offer created; app status moved to OFFERED | PASS |
| TC-OFF-02 | Offers | Block offer creation for non-SELECTED application | Application in APPLIED or SHORTLISTED status | Raise ValidationError: allowed only for SELECTED applications | ValidationError raised; offer blocked | PASS |
| TC-OFF-03 | Offers | Block offer with invalid joining date | Joining Date <= Offer Date | Raise ValidationError: joining date must be strictly after offer date | ValidationError raised; invalid dates rejected | PASS |
| TC-OFF-04 | Offers | Decline offer transitions application | Offer status set to DECLINED | Offer updated to DECLINED and application moves to REJECTED | Offer and application updated atomically | PASS |
| TC-PLC-01 | Placements | Record placement for OFFERED app with ACCEPTED offer | App status: OFFERED, Offer status: ACCEPTED | Placement created (PLC101), app moves to JOINED, openings decremented | Placement saved; app marked JOINED; vacancy decremented | PASS |
| TC-PLC-02 | Placements | Block placement when offer is not ACCEPTED | Offer status is OFFERED (pending response) | Raise ValidationError: requires accepted offer | ValidationError raised; placement blocked | PASS |
| TC-PLC-03 | Placements | Block duplicate placement for same application | Second placement recorded for same application | Raise ValidationError: placement already exists | ValidationError raised; duplicate blocked | PASS |
| TC-REP-01 | Reports | Unplaced candidates report criteria | Candidates with active status and no JOINED application | Returns only active students without a placement | Subquery accurately filters out placed students | PASS |

