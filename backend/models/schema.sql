-- =====================================================
-- ScholarTrack
-- Scholarship & Fellowship Deadline Tracker
-- MySQL Database Schema
-- =====================================================

CREATE DATABASE IF NOT EXISTS scholartrack_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE scholartrack_db;


-- =====================================================
-- 1. USERS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(254) NOT NULL UNIQUE,

    password_hash VARCHAR(255) NOT NULL,

    role ENUM('student', 'admin') NOT NULL DEFAULT 'student',

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_users_role (role),
    INDEX idx_users_active (is_active)
) ENGINE=InnoDB;


-- =====================================================
-- 2. STUDENT PROFILES TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS student_profiles (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    user_id BIGINT UNSIGNED NOT NULL UNIQUE,

    phone VARCHAR(20),

    date_of_birth DATE,

    gender VARCHAR(30),

    state VARCHAR(100),

    district VARCHAR(100),

    education_level VARCHAR(100),

    institution VARCHAR(200),

    course VARCHAR(150),

    specialization VARCHAR(150),

    study_year VARCHAR(30),

    marks_percentage DECIMAL(5,2),

    annual_family_income DECIMAL(14,2),

    category VARCHAR(50),

    preferred_categories JSON,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_profiles_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_marks_percentage
        CHECK (
            marks_percentage IS NULL
            OR marks_percentage BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_family_income
        CHECK (
            annual_family_income IS NULL
            OR annual_family_income >= 0
        )
) ENGINE=InnoDB;


-- =====================================================
-- 3. SCHOLARSHIP SOURCES TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS scholarship_sources (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    source_name VARCHAR(200) NOT NULL,

    source_url VARCHAR(500) NOT NULL UNIQUE,

    source_type ENUM(
        'government',
        'university',
        'foundation',
        'other'
    ) NOT NULL DEFAULT 'other',

    is_approved BOOLEAN NOT NULL DEFAULT FALSE,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    last_scraped_at DATETIME NULL,

    last_scrape_status ENUM(
        'success',
        'failed',
        'pending'
    ) NOT NULL DEFAULT 'pending',

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_sources_active (is_active),
    INDEX idx_sources_approved (is_approved)
) ENGINE=InnoDB;


-- =====================================================
-- 4. SCHOLARSHIPS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS scholarships (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    source_id BIGINT UNSIGNED NULL,

    external_id VARCHAR(255) NULL,

    title VARCHAR(300) NOT NULL,

    provider VARCHAR(255) NOT NULL,

    description TEXT,

    scholarship_type VARCHAR(100),

    education_level VARCHAR(150),

    eligible_courses TEXT,

    eligible_states JSON,

    eligible_categories JSON,

    minimum_marks DECIMAL(5,2),

    maximum_family_income DECIMAL(14,2),

    amount_min DECIMAL(14,2),

    amount_max DECIMAL(14,2),

    currency CHAR(3) NOT NULL DEFAULT 'INR',

    application_open_date DATE NULL,

    deadline DATE NULL,

    deadline_status ENUM(
        'known',
        'unknown',
        'not_applicable'
    ) NOT NULL DEFAULT 'unknown',

    official_url VARCHAR(2048) NOT NULL,

    application_url VARCHAR(2048),

    eligibility_details TEXT,

    required_documents JSON,

    is_verified BOOLEAN NOT NULL DEFAULT FALSE,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    last_checked_at DATETIME NULL,

    content_hash CHAR(64),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_scholarship_source
        FOREIGN KEY (source_id)
        REFERENCES scholarship_sources(id)
        ON DELETE SET NULL,

    CONSTRAINT chk_scholarship_minimum_marks
        CHECK (
            minimum_marks IS NULL
            OR minimum_marks BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_scholarship_amount_min
        CHECK (
            amount_min IS NULL
            OR amount_min >= 0
        ),

    CONSTRAINT chk_scholarship_amount_max
        CHECK (
            amount_max IS NULL
            OR amount_max >= 0
        ),

    UNIQUE KEY uq_source_external_id (
        source_id,
        external_id
    ),

    INDEX idx_scholarships_title (title),

    INDEX idx_scholarships_deadline (
        is_active,
        deadline
    ),

    INDEX idx_scholarships_education (
        education_level
    ),

    INDEX idx_scholarships_provider (
        provider
    ),

    INDEX idx_scholarships_verified (
        is_verified,
        is_active
    )
) ENGINE=InnoDB;


-- =====================================================
-- 5. SAVED SCHOLARSHIPS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS saved_scholarships (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    user_id BIGINT UNSIGNED NOT NULL,

    scholarship_id BIGINT UNSIGNED NOT NULL,

    saved_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_saved_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_saved_scholarship
        FOREIGN KEY (scholarship_id)
        REFERENCES scholarships(id)
        ON DELETE CASCADE,

    UNIQUE KEY uq_saved_user_scholarship (
        user_id,
        scholarship_id
    ),

    INDEX idx_saved_scholarship (scholarship_id)
) ENGINE=InnoDB;


-- =====================================================
-- 6. APPLICATIONS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS applications (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    user_id BIGINT UNSIGNED NOT NULL,

    scholarship_id BIGINT UNSIGNED NOT NULL,

    status ENUM(
        'interested',
        'preparing',
        'submitted',
        'under_review',
        'approved',
        'rejected',
        'withdrawn'
    ) NOT NULL DEFAULT 'interested',

    application_reference VARCHAR(255),

    applied_at DATETIME NULL,

    notes TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_application_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_application_scholarship
        FOREIGN KEY (scholarship_id)
        REFERENCES scholarships(id)
        ON DELETE RESTRICT,

    UNIQUE KEY uq_user_application (
        user_id,
        scholarship_id
    ),

    INDEX idx_applications_status (
        user_id,
        status
    ),

    INDEX idx_applications_applied_at (
        applied_at
    )
) ENGINE=InnoDB;


-- =====================================================
-- 7. SCHOLARSHIP CHANGE HISTORY
-- =====================================================

CREATE TABLE IF NOT EXISTS scholarship_change_history (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    scholarship_id BIGINT UNSIGNED NOT NULL,

    field_name VARCHAR(100) NOT NULL,

    old_value TEXT,

    new_value TEXT,

    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_change_scholarship
        FOREIGN KEY (scholarship_id)
        REFERENCES scholarships(id)
        ON DELETE CASCADE,

    INDEX idx_change_scholarship_date (
        scholarship_id,
        detected_at
    )
) ENGINE=InnoDB;


-- =====================================================
-- 8. SCRAPING LOGS
-- =====================================================

CREATE TABLE IF NOT EXISTS scraping_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    source_id BIGINT UNSIGNED NULL,

    started_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    finished_at DATETIME NULL,

    status ENUM(
        'running',
        'success',
        'failed'
    ) NOT NULL DEFAULT 'running',

    records_found INT UNSIGNED NOT NULL DEFAULT 0,

    records_inserted INT UNSIGNED NOT NULL DEFAULT 0,

    records_updated INT UNSIGNED NOT NULL DEFAULT 0,

    error_message TEXT, 

    CONSTRAINT fk_scraping_source
        FOREIGN KEY (source_id)
        REFERENCES scholarship_sources(id)
        ON DELETE SET NULL,

    INDEX idx_scraping_status (status),

    INDEX idx_scraping_started (started_at)
) ENGINE=InnoDB;


-- =====================================================
-- 9. NOTIFICATIONS
-- =====================================================

CREATE TABLE IF NOT EXISTS notifications (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    user_id BIGINT UNSIGNED NOT NULL,

    scholarship_id BIGINT UNSIGNED NULL,

    notification_type VARCHAR(100) NOT NULL,

    title VARCHAR(255) NOT NULL,

    message TEXT NOT NULL,

    is_read BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    read_at DATETIME NULL,

    CONSTRAINT fk_notification_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_notification_scholarship
        FOREIGN KEY (scholarship_id)
        REFERENCES scholarships(id)
        ON DELETE SET NULL,

    INDEX idx_notifications_user_read (
        user_id,
        is_read,
        created_at
    )
) ENGINE=InnoDB;


-- =====================================================
-- 10. ADMIN AUDIT LOGS
-- =====================================================

CREATE TABLE IF NOT EXISTS admin_audit_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    admin_user_id BIGINT UNSIGNED NULL,

    action VARCHAR(150) NOT NULL,

    entity_type VARCHAR(100),

    entity_id BIGINT UNSIGNED NULL,

    details JSON,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_admin
        FOREIGN KEY (admin_user_id)
        REFERENCES users(id)
        ON DELETE SET NULL,

    INDEX idx_audit_admin_date (
        admin_user_id,
        created_at
    ),

    INDEX idx_audit_entity (
        entity_type,
        entity_id
    )
) ENGINE=InnoDB;