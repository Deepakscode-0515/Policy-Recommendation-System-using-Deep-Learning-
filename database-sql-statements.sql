-- ============================================================================
-- INSURANCE POLICY RECOMMENDATION APPLICATION
-- Complete Database Schema and SQL Statements
-- Database: insurance_app
-- MySQL 8.0+
-- ============================================================================

-- ============================================================================
-- 1. MAIN TABLES - TABLE CREATION STATEMENTS
-- ============================================================================

-- 1.1 USERS TABLE
-- Stores user authentication and account information
-- Purpose: Manage user registration, login, and account lifecycle
-- Indexes: email (unique), id (primary key)

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 1.2 PROFILES TABLE
-- Stores user demographic and health profile information
-- Purpose: Maintain user personal details for RAF calculation and assessment
-- Fields:
--   - full_name: User's full name (required)
--   - age: Age in years (required)
--   - gender: male, female, or other (required)
--   - health_issues: Comma-separated or free-text health conditions (optional)
--   - smoking: Binary flag (0=no, 1=yes) (default: 0)
--   - alcohol: Binary flag (0=no, 1=yes) (default: 0)
--   - annual_income_inr: Annual income in Indian Rupees (required)
--   - updated_at: Last update timestamp (auto-managed)
-- Indexes: user_id (foreign key), updated_at

CREATE TABLE profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    health_issues TEXT NULL,
    smoking TINYINT(1) NOT NULL DEFAULT 0,
    alcohol TINYINT(1) NOT NULL DEFAULT 0,
    annual_income_inr BIGINT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_profiles_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 1.3 ASSESSMENTS TABLE
-- Stores assessment results, RAF scores, and AI-generated recommendations
-- Purpose: Track all health assessments, RAF computations, and policy recommendations per user
-- Fields:
--   - user_id: Foreign key to users table
--   - raf_score: Risk Assessment Factor score (0.0 to 1.0, stored as FLOAT)
--   - input_snapshot_json: Complete user profile snapshot at time of assessment (JSON format as TEXT)
--   - output_json: Complete Gemini AI response with insights and recommendations (JSON format as TEXT)
--   - created_at: Assessment timestamp (auto-managed, indexed for sorting)
-- Indexes: user_id (foreign key), created_at (for recent activity queries)

CREATE TABLE assessments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    raf_score FLOAT NOT NULL,
    input_snapshot_json TEXT NOT NULL,
    output_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_assessments_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_user_created (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 2. MIGRATION AND ALTERATION STATEMENTS
-- ============================================================================

-- 2.1 MIGRATION: Fix Profile Columns (20251011_fix_profiles_columns.sql)
-- Renames columns to match SQLAlchemy ORM model
-- Apply this if your schema has old column names

ALTER TABLE profiles
  CHANGE COLUMN medical_history health_issues TEXT NULL;

ALTER TABLE profiles
  CHANGE COLUMN smoker smoking TINYINT(1) NOT NULL DEFAULT 0;

ALTER TABLE profiles
  MODIFY COLUMN alcohol TINYINT(1) NOT NULL DEFAULT 0;

-- 2.2 MIGRATION: Add Assessment JSON Columns (20251011_add_assessment_json_columns.sql)
-- Adds JSON storage columns for input snapshots and AI output
-- Apply this if your assessments table lacks these columns

ALTER TABLE assessments
  ADD COLUMN input_snapshot_json TEXT NULL AFTER raf_score;

ALTER TABLE assessments
  ADD COLUMN output_json TEXT NULL AFTER input_snapshot_json;

-- ============================================================================
-- 3. VERIFICATION QUERIES
-- ============================================================================

-- 3.1 Check database and tables exist
USE insurance_app;
SHOW TABLES;

-- 3.2 Describe table structures
DESCRIBE users;
DESCRIBE profiles;
DESCRIBE assessments;

-- 3.3 View column details and constraints
SELECT 
    COLUMN_NAME, 
    COLUMN_TYPE, 
    IS_NULLABLE, 
    COLUMN_KEY, 
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'users' AND TABLE_SCHEMA = 'insurance_app'
ORDER BY ORDINAL_POSITION;

SELECT 
    COLUMN_NAME, 
    COLUMN_TYPE, 
    IS_NULLABLE, 
    COLUMN_KEY, 
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'profiles' AND TABLE_SCHEMA = 'insurance_app'
ORDER BY ORDINAL_POSITION;

SELECT 
    COLUMN_NAME, 
    COLUMN_TYPE, 
    IS_NULLABLE, 
    COLUMN_KEY, 
    COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'assessments' AND TABLE_SCHEMA = 'insurance_app'
ORDER BY ORDINAL_POSITION;

-- ============================================================================
-- 4. INDEX STATEMENTS
-- ============================================================================

-- 4.1 Foreign Key Indexes (for relationship queries)
CREATE INDEX idx_profiles_user_id ON profiles(user_id);
CREATE INDEX idx_assessments_user_id ON assessments(user_id);

-- 4.2 Temporal Indexes (for sorting and filtering by date)
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_profiles_updated_at ON profiles(updated_at);
CREATE INDEX idx_assessments_created_at ON assessments(created_at);

-- 4.3 Composite Index (for recent activity queries)
CREATE INDEX idx_assessments_user_created ON assessments(user_id, created_at DESC);

-- 4.4 Unique Constraints (for data integrity)
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_profiles_user_id_unique ON profiles(user_id);

-- ============================================================================
-- 5. SAMPLE DATA QUERIES (FOR TESTING/DEVELOPMENT)
-- ============================================================================

-- 5.1 Insert sample user
INSERT INTO users (email, password_hash) 
VALUES ('test@example.com', 'hashed_password_here');

-- 5.2 Insert sample profile
INSERT INTO profiles (user_id, full_name, age, gender, health_issues, smoking, alcohol, annual_income_inr)
VALUES (1, 'John Doe', 45, 'male', 'Diabetes, Hypertension', 1, 0, 800000);

-- 5.3 Insert sample assessment
INSERT INTO assessments (user_id, raf_score, input_snapshot_json, output_json)
VALUES (
    1, 
    0.65, 
    '{"age": 45, "gender": "male", "health_issues": "Diabetes, Hypertension", "smoking": true, "alcohol": false, "annual_income_inr": 800000}',
    '{"insights": "High cardiovascular risk", "recommendations": ["Term Insurance", "Health Insurance"], "policies": [...]}'
);

-- ============================================================================
-- 6. DATA MAINTENANCE QUERIES
-- ============================================================================

-- 6.1 Update user profile
UPDATE profiles 
SET health_issues = 'Diabetes', smoking = 0, alcohol = 1, updated_at = CURRENT_TIMESTAMP
WHERE user_id = 1;

-- 6.2 Delete assessment by ID
DELETE FROM assessments WHERE id = 5;

-- 6.3 Delete all assessments for a user
DELETE FROM assessments WHERE user_id = 1;

-- 6.4 Get recent assessments for a user (most recent first)
SELECT * FROM assessments 
WHERE user_id = 1 
ORDER BY created_at DESC 
LIMIT 10;

-- 6.5 Get user profile summary with assessment count
SELECT 
    u.id, 
    u.email, 
    p.full_name, 
    p.age, 
    p.gender, 
    COUNT(a.id) as assessment_count,
    MAX(a.created_at) as latest_assessment_date
FROM users u
LEFT JOIN profiles p ON u.id = p.user_id
LEFT JOIN assessments a ON u.id = a.user_id
GROUP BY u.id
ORDER BY u.created_at DESC;

-- 6.6 Get assessment details with RAF score
SELECT 
    a.id,
    a.user_id,
    u.email,
    a.raf_score,
    a.created_at,
    JSON_EXTRACT(a.input_snapshot_json, '$.age') as age,
    JSON_EXTRACT(a.input_snapshot_json, '$.health_issues') as health_issues
FROM assessments a
JOIN users u ON a.user_id = u.id
WHERE a.user_id = 1
ORDER BY a.created_at DESC;

-- ============================================================================
-- 7. BACKUP AND RESTORE QUERIES
-- ============================================================================

-- 7.1 Export data to CSV (from MySQL CLI)
-- SELECT * FROM users INTO OUTFILE '/tmp/users_backup.csv' 
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

-- 7.2 Drop all tables (WARNING: Destructive - use for reset only)
-- DROP TABLE IF EXISTS assessments;
-- DROP TABLE IF EXISTS profiles;
-- DROP TABLE IF EXISTS users;

-- 7.3 Truncate data but keep schema (WARNING: Destructive)
-- TRUNCATE TABLE assessments;
-- TRUNCATE TABLE profiles;
-- TRUNCATE TABLE users;

-- ============================================================================
-- 8. SUMMARY OF DATABASE STRUCTURE
-- ============================================================================
-- 
-- USERS (3 fields):
--   - id (PK), email (UNIQUE), password_hash, created_at
--
-- PROFILES (1-to-1 with USERS):
--   - id (PK), user_id (FK), full_name, age, gender, health_issues, 
--     smoking, alcohol, annual_income_inr, updated_at
--
-- ASSESSMENTS (1-to-many with USERS):
--   - id (PK), user_id (FK), raf_score, input_snapshot_json, 
--     output_json, created_at
--
-- RELATIONSHIPS:
--   - users.id → profiles.user_id (1-to-1)
--   - users.id → assessments.user_id (1-to-many)
--   - CASCADE DELETE enabled (orphaned profiles/assessments deleted with user)
--
-- KEY OPERATIONS:
--   - Register: INSERT into users
--   - Update Profile: UPDATE profiles by user_id
--   - Create Assessment: INSERT into assessments with JSON snapshots
--   - View Recent Activity: SELECT from assessments ORDER BY created_at DESC
--   - Delete Assessment: DELETE from assessments by id
--
-- ============================================================================
