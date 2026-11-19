-- TalentLoop Database Schema
-- Recruitment & Placement Management System

CREATE DATABASE IF NOT EXISTS talentloop_db;
USE talentloop_db;

DROP TABLE IF EXISTS placements;
DROP TABLE IF EXISTS offers;
DROP TABLE IF EXISTS interview_feedback;
DROP TABLE IF EXISTS interviews;
DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS candidates;

CREATE TABLE candidates (
    candidate_id VARCHAR(16) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    mobile VARCHAR(10) NOT NULL,
    technology VARCHAR(50) NOT NULL,
    percentage DECIMAL(5, 2) NOT NULL,
    passing_year INT NOT NULL,
    backlog_count INT NOT NULL DEFAULT 0,
    is_active TINYINT NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (candidate_id),
    UNIQUE KEY uq_candidate_email (email),
    UNIQUE KEY uq_candidate_mobile (mobile),
    CONSTRAINT chk_candidate_percentage CHECK (percentage BETWEEN 0.00 AND 100.00),
    CONSTRAINT chk_candidate_backlogs CHECK (backlog_count >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE companies (
    company_id VARCHAR(16) NOT NULL,
    name VARCHAR(100) NOT NULL,
    industry VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    contact_person VARCHAR(100) NOT NULL,
    contact_email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (company_id),
    UNIQUE KEY uq_company_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE jobs (
    job_id VARCHAR(16) NOT NULL,
    company_id VARCHAR(16) NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    technology VARCHAR(50) NOT NULL,
    openings INT NOT NULL,
    location VARCHAR(50) NOT NULL,
    package_lpa DECIMAL(5, 2) NOT NULL,
    min_percentage DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    passing_year INT NOT NULL,
    max_backlogs INT NOT NULL DEFAULT 0,
    deadline DATE NOT NULL,
    status ENUM('OPEN', 'CLOSED') NOT NULL DEFAULT 'OPEN',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (job_id),
    CONSTRAINT chk_job_openings CHECK (openings > 0),
    CONSTRAINT chk_job_package CHECK (package_lpa >= 0.00),
    CONSTRAINT chk_job_min_percentage CHECK (min_percentage BETWEEN 0.00 AND 100.00),
    CONSTRAINT chk_job_max_backlogs CHECK (max_backlogs >= 0),
    CONSTRAINT fk_jobs_company FOREIGN KEY (company_id)
        REFERENCES companies (company_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE applications (
    application_id VARCHAR(16) NOT NULL,
    candidate_id VARCHAR(16) NOT NULL,
    job_id VARCHAR(16) NOT NULL,
    applied_date DATE NOT NULL,
    status ENUM('APPLIED', 'SHORTLISTED', 'INTERVIEW', 'SELECTED', 'OFFERED', 'JOINED', 'REJECTED') NOT NULL DEFAULT 'APPLIED',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (application_id),
    UNIQUE KEY uq_candidate_job (candidate_id, job_id),
    CONSTRAINT fk_applications_candidate FOREIGN KEY (candidate_id)
        REFERENCES candidates (candidate_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_applications_job FOREIGN KEY (job_id)
        REFERENCES jobs (job_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE interviews (
    interview_id VARCHAR(16) NOT NULL,
    application_id VARCHAR(16) NOT NULL,
    round_no INT NOT NULL DEFAULT 1,
    interview_date DATE NOT NULL,
    mode ENUM('Online', 'Offline') NOT NULL DEFAULT 'Online',
    interviewer VARCHAR(100) NOT NULL,
    status ENUM('SCHEDULED', 'COMPLETED', 'CANCELLED') NOT NULL DEFAULT 'SCHEDULED',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (interview_id),
    CONSTRAINT chk_interview_round CHECK (round_no > 0),
    CONSTRAINT fk_interviews_application FOREIGN KEY (application_id)
        REFERENCES applications (application_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE interview_feedback (
    feedback_id VARCHAR(16) NOT NULL,
    interview_id VARCHAR(16) NOT NULL,
    technical_rating INT NOT NULL,
    communication_rating INT NOT NULL,
    remarks TEXT,
    result ENUM('PASS', 'FAIL') NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (feedback_id),
    CONSTRAINT chk_feedback_tech_rating CHECK (technical_rating BETWEEN 1 AND 10),
    CONSTRAINT chk_feedback_comm_rating CHECK (communication_rating BETWEEN 1 AND 10),
    CONSTRAINT fk_feedback_interview FOREIGN KEY (interview_id)
        REFERENCES interviews (interview_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE offers (
    offer_id VARCHAR(16) NOT NULL,
    application_id VARCHAR(16) NOT NULL,
    designation VARCHAR(100) NOT NULL,
    package_lpa DECIMAL(5, 2) NOT NULL,
    offer_date DATE NOT NULL,
    joining_date DATE NOT NULL,
    offer_status ENUM('OFFERED', 'ACCEPTED', 'DECLINED') NOT NULL DEFAULT 'OFFERED',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (offer_id),
    CONSTRAINT chk_offer_package CHECK (package_lpa >= 0.00),
    CONSTRAINT fk_offers_application FOREIGN KEY (application_id)
        REFERENCES applications (application_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE placements (
    placement_id VARCHAR(16) NOT NULL,
    application_id VARCHAR(16) NOT NULL,
    company_id VARCHAR(16) NOT NULL,
    designation VARCHAR(100) NOT NULL,
    final_package_lpa DECIMAL(5, 2) NOT NULL,
    actual_joining_date DATE,
    joining_status ENUM('JOINED', 'NOT_JOINED') NOT NULL DEFAULT 'JOINED',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (placement_id),
    CONSTRAINT chk_placement_package CHECK (final_package_lpa >= 0.00),
    CONSTRAINT fk_placements_application FOREIGN KEY (application_id)
        REFERENCES applications (application_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_placements_company FOREIGN KEY (company_id)
        REFERENCES companies (company_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Indexes on frequently searched columns
CREATE INDEX idx_candidates_technology ON candidates (technology);
CREATE INDEX idx_jobs_status ON jobs (status);
CREATE INDEX idx_applications_status ON applications (status);
