-- TalentLoop Sample Data
-- Realistic Indian recruitment & placement sample data

USE talentloop_db;

-- Clear existing data in reverse dependency order
DELETE FROM placements;
DELETE FROM offers;
DELETE FROM interview_feedback;
DELETE FROM interviews;
DELETE FROM applications;
DELETE FROM jobs;
DELETE FROM companies;
DELETE FROM candidates;

-- 1. Candidates
INSERT INTO candidates (candidate_id, name, email, mobile, technology, percentage, passing_year, backlog_count, is_active) VALUES
('CAN1001', 'Aarav Sharma', 'aarav.sharma@gmail.com', '9820011001', 'Java', 78.50, 2024, 0, 1),
('CAN1002', 'Priya Patel', 'priya.patel@gmail.com', '9820011002', 'Python', 82.00, 2024, 0, 1),
('CAN1003', 'Rohan Deshmukh', 'rohan.deshmukh@gmail.com', '9820011003', 'Java', 68.40, 2023, 1, 1),
('CAN1004', 'Sneha Kulkarni', 'sneha.kulkarni@gmail.com', '9820011004', 'React', 85.20, 2024, 0, 1),
('CAN1005', 'Aditya Verma', 'aditya.verma@gmail.com', '9820011005', 'Python', 74.00, 2023, 0, 1),
('CAN1006', 'Neha Joshi', 'neha.joshi@gmail.com', '9820011006', 'Data Science', 88.60, 2024, 0, 1),
('CAN1007', 'Vikram Malhotra', 'vikram.malhotra@gmail.com', '9820011007', 'Java', 65.00, 2023, 2, 1),
('CAN1008', 'Ananya Iyer', 'ananya.iyer@gmail.com', '9820011008', 'React', 79.80, 2024, 0, 1),
('CAN1009', 'Siddharth Shinde', 'siddharth.shinde@gmail.com', '9820011009', 'Python', 71.50, 2024, 1, 1),
('CAN1010', 'Pooja Nair', 'pooja.nair@gmail.com', '9820011010', 'QA Testing', 76.20, 2023, 0, 1),
('CAN1011', 'Rahul Mehta', 'rahul.mehta@gmail.com', '9820011011', 'Java', 80.00, 2024, 0, 1),
('CAN1012', 'Tanvi Patil', 'tanvi.patil@gmail.com', '9820011012', 'Data Science', 83.40, 2024, 0, 1),
('CAN1013', 'Amit Jadhav', 'amit.jadhav@gmail.com', '9820011013', 'DevOps', 72.10, 2023, 0, 1),
('CAN1014', 'Divya Choudhary', 'divya.choudhary@gmail.com', '9820011014', 'QA Testing', 69.50, 2024, 0, 1),
('CAN1015', 'Kunal Verma', 'kunal.verma@gmail.com', '9820011015', 'Python', 79.50, 2024, 0, 1),
('CAN1016', 'Ritu Sen', 'ritu.sen@gmail.com', '9820011016', 'Java', 74.20, 2023, 1, 1),
('CAN1017', 'Manish Gupta', 'manish.gupta@gmail.com', '9820011017', 'React', 81.00, 2024, 0, 1),
('CAN1018', 'Shruti Thorat', 'shruti.thorat@gmail.com', '9820011018', 'Data Science', 86.40, 2024, 0, 1),
('CAN1019', 'Abhishek Pandey', 'abhishek.pandey@gmail.com', '9820011019', 'DevOps', 70.80, 2023, 0, 1),
('CAN1020', 'Kavita Waghmare', 'kavita.waghmare@gmail.com', '9820011020', 'QA Testing', 73.50, 2024, 0, 1),
('CAN1021', 'Prateek Mishra', 'prateek.mishra@gmail.com', '9820011021', 'Java', 83.20, 2024, 0, 1),
('CAN1022', 'Sayali Gaikwad', 'sayali.gaikwad@gmail.com', '9820011022', 'Python', 77.90, 2023, 0, 1),
('CAN1023', 'Varun Bhatnagar', 'varun.bhatnagar@gmail.com', '9820011023', 'React', 67.50, 2023, 2, 1),
('CAN1024', 'Megha Shrivastava', 'megha.s@gmail.com', '9820011024', 'Data Science', 89.10, 2024, 0, 1),
('CAN1025', 'Darshan Solanki', 'darshan.solanki@gmail.com', '9820011025', 'Java', 75.60, 2024, 0, 1),
('CAN1026', 'Ankita More', 'ankita.more@gmail.com', '9820011026', 'Python', 84.30, 2024, 0, 1),
('CAN1027', 'Nikhil Sawant', 'nikhil.sawant@gmail.com', '9820011027', 'DevOps', 71.00, 2023, 1, 1),
('CAN1028', 'Pallavi Rao', 'pallavi.rao@gmail.com', '9820011028', 'React', 78.40, 2024, 0, 1),
('CAN1029', 'Gaurav Kadam', 'gaurav.kadam@gmail.com', '9820011029', 'QA Testing', 68.00, 2023, 0, 1),
('CAN1030', 'Komal Bhalerao', 'komal.bhalerao@gmail.com', '9820011030', 'Java', 82.50, 2024, 0, 1),
('CAN1031', 'Sanket Mahajan', 'sanket.mahajan@gmail.com', '9820011031', 'Python', 69.20, 2024, 1, 1),
('CAN1032', 'Shweta Kamble', 'shweta.kamble@gmail.com', '9820011032', 'Data Science', 87.00, 2024, 0, 1),
('CAN1033', 'Tejas Salunkhe', 'tejas.salunkhe@gmail.com', '9820011033', 'React', 76.80, 2023, 0, 1),
('CAN1034', 'Isha Tambe', 'isha.tambe@gmail.com', '9820011034', 'DevOps', 80.40, 2024, 0, 1);

-- 2. Companies
INSERT INTO companies (company_id, name, industry, location, contact_person, contact_email) VALUES
('COM101', 'Tata Consultancy Services', 'IT Services', 'Pune', 'Rajesh Kulkarni', 'rajesh.kulkarni@tcs.com'),
('COM102', 'Infosys Limited', 'IT Consulting', 'Bengaluru', 'Sangeeta Rao', 'sangeeta.rao@infosys.com'),
('COM103', 'Persistent Systems', 'Software Product Engineering', 'Pune', 'Anand Gokhale', 'anand.gokhale@persistent.com'),
('COM104', 'Wipro Technologies', 'Cloud & Digital Services', 'Hyderabad', 'Meenakshi Sundaram', 'meenakshi.s@wipro.com'),
('COM105', 'Zensar Technologies', 'Enterprise Solutions', 'Pune', 'Harish Bhat', 'harish.bhat@zensar.com'),
('COM106', 'Cognizant Technology Solutions', 'IT & Consulting', 'Chennai', 'Suresh Narayanan', 'suresh.n@cognizant.com');

-- 3. Jobs
INSERT INTO jobs (job_id, company_id, job_title, technology, openings, location, package_lpa, min_percentage, passing_year, max_backlogs, deadline, status) VALUES
('JOB101', 'COM101', 'Java Backend Developer', 'Java', 5, 'Pune', 4.50, 65.00, 2024, 0, '2026-12-31', 'OPEN'),
('JOB102', 'COM101', 'Python Data Engineer', 'Python', 3, 'Pune', 5.20, 70.00, 2024, 0, '2026-12-31', 'OPEN'),
('JOB103', 'COM102', 'Full Stack React Developer', 'React', 4, 'Bengaluru', 5.00, 68.00, 2024, 1, '2026-12-15', 'OPEN'),
('JOB104', 'COM102', 'Systems Engineer - Java', 'Java', 10, 'Pune', 4.00, 60.00, 2023, 1, '2026-12-20', 'OPEN'),
('JOB105', 'COM103', 'Associate Software Engineer', 'Python', 4, 'Pune', 6.00, 75.00, 2024, 0, '2026-12-25', 'OPEN'),
('JOB106', 'COM104', 'QA Automation Engineer', 'QA Testing', 3, 'Hyderabad', 4.20, 65.00, 2023, 0, '2026-11-30', 'OPEN'),
('JOB107', 'COM105', 'Junior Data Scientist', 'Data Science', 2, 'Pune', 6.50, 75.00, 2024, 0, '2026-12-10', 'OPEN'),
('JOB108', 'COM106', 'Cloud & DevOps Associate', 'DevOps', 2, 'Chennai', 5.50, 70.00, 2023, 0, '2026-11-15', 'CLOSED'),
('JOB109', 'COM103', 'Frontend React Engineer', 'React', 3, 'Pune', 5.50, 70.00, 2024, 0, '2026-12-30', 'OPEN');

-- 4. Applications
INSERT INTO applications (application_id, candidate_id, job_id, applied_date, status) VALUES
('APP501', 'CAN1001', 'JOB101', '2026-10-01', 'JOINED'),
('APP502', 'CAN1002', 'JOB102', '2026-10-05', 'OFFERED'),
('APP503', 'CAN1003', 'JOB104', '2026-10-10', 'SELECTED'),
('APP504', 'CAN1004', 'JOB103', '2026-10-12', 'INTERVIEW'),
('APP505', 'CAN1005', 'JOB105', '2026-10-15', 'SHORTLISTED'),
('APP506', 'CAN1006', 'JOB107', '2026-10-18', 'APPLIED'),
('APP507', 'CAN1007', 'JOB101', '2026-10-02', 'REJECTED'),
('APP508', 'CAN1008', 'JOB109', '2026-10-20', 'JOINED'),
('APP509', 'CAN1009', 'JOB102', '2026-10-22', 'INTERVIEW'),
('APP510', 'CAN1010', 'JOB106', '2026-10-25', 'OFFERED'),
('APP511', 'CAN1011', 'JOB101', '2026-10-26', 'SHORTLISTED'),
('APP512', 'CAN1012', 'JOB107', '2026-10-28', 'REJECTED'),
('APP513', 'CAN1013', 'JOB108', '2026-10-15', 'APPLIED'),
('APP514', 'CAN1014', 'JOB106', '2026-10-29', 'APPLIED');

-- 5. Interviews
INSERT INTO interviews (interview_id, application_id, round_no, interview_date, mode, interviewer, status) VALUES
('INT101', 'APP501', 1, '2026-10-08', 'Online', 'Nitin Gadgil', 'COMPLETED'),
('INT102', 'APP501', 2, '2026-10-12', 'Offline', 'Sunil Joshi', 'COMPLETED'),
('INT103', 'APP508', 1, '2026-10-24', 'Online', 'Deepak Verma', 'COMPLETED'),
('INT104', 'APP502', 1, '2026-10-14', 'Online', 'Kavita Menon', 'COMPLETED'),
('INT105', 'APP510', 1, '2026-10-30', 'Online', 'Ramesh Sen', 'COMPLETED'),
('INT106', 'APP503', 1, '2026-10-18', 'Offline', 'Praveen Bansal', 'COMPLETED'),
('INT107', 'APP504', 1, '2026-11-22', 'Online', 'Arjun Saxena', 'SCHEDULED'),
('INT108', 'APP509', 1, '2026-11-25', 'Online', 'Nitin Gadgil', 'SCHEDULED'),
('INT109', 'APP507', 1, '2026-10-06', 'Offline', 'Sunil Joshi', 'COMPLETED'),
('INT110', 'APP512', 1, '2026-10-30', 'Online', 'Kavita Menon', 'COMPLETED');

-- 6. Interview Feedback
INSERT INTO interview_feedback (feedback_id, interview_id, technical_rating, communication_rating, remarks, result) VALUES
('FB101', 'INT101', 8, 8, 'Strong in Core Java and object-oriented design.', 'PASS'),
('FB102', 'INT102', 9, 8, 'Excellent problem solving and clear communication.', 'PASS'),
('FB103', 'INT103', 8, 9, 'Great grasp of React lifecycle and modern state management.', 'PASS'),
('FB104', 'INT104', 8, 9, 'Solid understanding of Python algorithms and relational queries.', 'PASS'),
('FB105', 'INT105', 7, 8, 'Good foundation in test case design and Selenium automation.', 'PASS'),
('FB106', 'INT106', 7, 7, 'Cleared technical assessment and coding round successfully.', 'PASS'),
('FB107', 'INT109', 4, 5, 'Foundations in OOP and data structures need significant improvement.', 'FAIL'),
('FB108', 'INT110', 4, 6, 'Lacks practical project experience with requested machine learning workflows.', 'FAIL');

-- 7. Offers
INSERT INTO offers (offer_id, application_id, designation, package_lpa, offer_date, joining_date, offer_status) VALUES
('OFF101', 'APP501', 'Associate Software Engineer - Java', 4.50, '2026-10-16', '2026-11-01', 'ACCEPTED'),
('OFF102', 'APP508', 'Junior Frontend Developer', 5.50, '2026-10-28', '2026-11-10', 'ACCEPTED'),
('OFF103', 'APP502', 'Data Engineer Trainee', 5.20, '2026-10-20', '2026-12-01', 'OFFERED'),
('OFF104', 'APP510', 'Associate QA Engineer', 4.20, '2026-11-05', '2026-12-15', 'OFFERED');

-- 8. Placements
INSERT INTO placements (placement_id, application_id, company_id, designation, final_package_lpa, actual_joining_date, joining_status) VALUES
('PLC101', 'APP501', 'COM101', 'Associate Software Engineer - Java', 4.50, '2026-11-01', 'JOINED'),
('PLC102', 'APP508', 'COM103', 'Junior Frontend Developer', 5.50, '2026-11-10', 'JOINED');

