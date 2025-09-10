-- Initialize Monopoly Deal Database
-- This script sets up the initial database structure and data

-- Create database if it doesn't exist (handled by Docker)
-- CREATE DATABASE IF NOT EXISTS monopoly_deal;

-- Set timezone
SET timezone = 'UTC';

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The tables will be created by SQLAlchemy/Alembic
-- This file can be used for initial data seeding

-- Insert initial configuration presets (will be handled by the application)
-- The application will create these automatically via the ConfigurationManager

-- Create indexes for better performance (will be added later via migrations)
-- CREATE INDEX IF NOT EXISTS idx_game_analyses_user_id ON game_analyses(user_id);
-- CREATE INDEX IF NOT EXISTS idx_game_analyses_created_at ON game_analyses(created_at);
-- CREATE INDEX IF NOT EXISTS idx_configuration_presets_official ON configuration_presets(is_official);
-- CREATE INDEX IF NOT EXISTS idx_user_configurations_user_id ON user_configurations(user_id);

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'Monopoly Deal database initialization completed at %', NOW();
END $$;