-- Phase 1: Committee Excellence Initiative - Schema Overhaul
-- This script creates the necessary tables for the new editorial workflow.
-- It is designed to be idempotent.

BEGIN;

-- Table to assign editors to specific committees
CREATE TABLE IF NOT EXISTS committee_editors (
    id SERIAL PRIMARY KEY,
    committee_id INT NOT NULL,
    editor_user_id INT NOT NULL,
    authority_level VARCHAR(20) NOT NULL DEFAULT 'reviewer', -- e.g., 'primary', 'secondary', 'reviewer'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(committee_id, editor_user_id)
);

COMMENT ON TABLE committee_editors IS 'Assigns users as editors for specific committees with defined authority levels.';

-- New table for curated member assignments with status and authority
CREATE TABLE IF NOT EXISTS member_assignments (
    id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    committee_id INT NOT NULL,
    assignment_type VARCHAR(50) NOT NULL DEFAULT 'member', -- e.g., 'chair', 'ranking_member', 'member'
    authority_source VARCHAR(50) NOT NULL DEFAULT 'editorial', -- e.g., 'editorial', 'official_source', 'scraped'
    confidence_score SMALLINT DEFAULT 100 CHECK (confidence_score >= 0 AND confidence_score <= 100),
    verified_by INT, -- user_id of the editor who verified this assignment
    verified_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) NOT NULL DEFAULT 'draft', -- e.g., 'draft', 'review', 'published'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(member_id, committee_id)
);

COMMENT ON TABLE member_assignments IS 'Stores curated committee member assignments with status, authority, and verification details.';

-- Table to log all changes to assignments for a full audit trail
CREATE TABLE IF NOT EXISTS assignment_changes (
    id SERIAL PRIMARY KEY,
    assignment_id INT NOT NULL,
    change_type VARCHAR(20) NOT NULL, -- e.g., 'create', 'update', 'delete', 'status_change'
    old_value JSONB,
    new_value JSONB,
    changed_by INT, -- user_id of the editor who made the change
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE assignment_changes IS 'Provides a complete audit trail for all changes to member assignments.';

-- Create a trigger function to automatically update the 'updated_at' timestamp
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply the trigger to the tables
DROP TRIGGER IF EXISTS update_committee_editors_modtime ON committee_editors;
CREATE TRIGGER update_committee_editors_modtime
    BEFORE UPDATE ON committee_editors
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

DROP TRIGGER IF EXISTS update_member_assignments_modtime ON member_assignments;
CREATE TRIGGER update_member_assignments_modtime
    BEFORE UPDATE ON member_assignments
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

COMMIT;

-- Post-creation verification
\echo "Schema overhaul script executed."
\echo "Tables created: committee_editors, member_assignments, assignment_changes."
