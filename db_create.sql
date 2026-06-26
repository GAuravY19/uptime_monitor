-- ==========================================
-- Table 1: Website Listing
-- Stores the websites registered by users
-- ==========================================

CREATE TABLE website_listing (
    web_id SERIAL PRIMARY KEY,
    web_name VARCHAR(255) NOT NULL UNIQUE,
    web_url TEXT NOT NULL,
    under_track BOOLEAN NOT NULL DEFAULT TRUE
);

-- ==========================================
-- Table 2: Website Tracking
-- Stores every monitoring attempt
-- ==========================================

CREATE TABLE website_tracking (
    track_id SERIAL PRIMARY KEY,
    web_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    status VARCHAR(10) NOT NULL
        CHECK (status IN ('UP', 'DOWN')),
    response_time_ms INTEGER,
    hit_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_web_id
        FOREIGN KEY (web_id)
        REFERENCES website_listing(web_id)
        ON DELETE CASCADE
);

BEGIN;

-- Step 1: Drop the foreign key constraint from the tracking table
ALTER TABLE website_tracking
    DROP CONSTRAINT fk_web_id;

-- Step 2: Remove the auto-increment (sequence) default from the listing table
ALTER TABLE website_listing
    ALTER COLUMN web_id DROP DEFAULT;

-- Step 3: Change the data type in the parent table (website_listing)
-- (Using explicit type casting to convert existing integers to strings safely)
ALTER TABLE website_listing
    ALTER COLUMN web_id TYPE VARCHAR(10) USING web_id::VARCHAR(10);

-- Step 4: Change the data type in the child table (website_tracking) to match perfectly
ALTER TABLE website_tracking
    ALTER COLUMN web_id TYPE VARCHAR(10) USING web_id::VARCHAR(10);

-- Step 5: Re-create the foreign key constraint with your original ON DELETE CASCADE rule
ALTER TABLE website_tracking
    ADD CONSTRAINT fk_web_id
    FOREIGN KEY (web_id)
    REFERENCES website_listing(web_id)
    ON DELETE CASCADE;

COMMIT;

ALTER TABLE website_tracking
ADD COLUMN response_difference INTEGER;


ALTER TABLE website_tracking
ADD COLUMN status_code INTEGER;
