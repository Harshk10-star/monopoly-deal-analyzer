"""Add configuration tables

Revision ID: add_configuration_tables
Revises: 
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_configuration_tables'
down_revision = None
depends_on = None


def upgrade():
    # Create configuration_presets table
    op.create_table('configuration_presets',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('rules_json', sa.JSON(), nullable=False),
        sa.Column('is_official', sa.Boolean(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('usage_count', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create user_configurations table
    op.create_table('user_configurations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('preset_id', sa.String(), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=True),
        sa.Column('last_used', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['preset_id'], ['configuration_presets.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Insert official presets
    op.execute("""
        INSERT INTO configuration_presets (id, name, description, rules_json, is_official, usage_count) VALUES
        ('strict_official', 'Strict Official Rules', 'Conservative interpretation following official rules closely', 
         '{"housePayment": "bank", "hotelMove": "not_allowed", "deckExhaustion": "reshuffle", "extraProperties": "cap", "buildingForfeiture": "discard", "propertyMerging": "auto_merge", "quadrupleRent": false, "forcedDealToDealBreaker": false, "justSayNoEmptyHand": false, "justSayNoOnZero": false}', 
         true, 0),
        ('flexible_house_rules', 'Flexible House Rules', 'More permissive rules allowing advanced strategies and edge case exploitation', 
         '{"housePayment": "floating", "hotelMove": "costs_action", "deckExhaustion": "reshuffle", "extraProperties": "split", "buildingForfeiture": "to_bank", "propertyMerging": "manual_merge", "quadrupleRent": true, "forcedDealToDealBreaker": true, "justSayNoEmptyHand": true, "justSayNoOnZero": true}', 
         true, 0),
        ('balanced_competitive', 'Balanced Competitive', 'Tournament-style rules balancing strategy depth with game flow', 
         '{"housePayment": "incomplete_set", "hotelMove": "costs_action", "deckExhaustion": "reshuffle", "extraProperties": "cap", "buildingForfeiture": "to_bank", "propertyMerging": "auto_merge", "quadrupleRent": false, "forcedDealToDealBreaker": true, "justSayNoEmptyHand": true, "justSayNoOnZero": false}', 
         true, 0),
        ('defensive_play', 'Defensive Play Style', 'Rules favoring defensive strategies and property protection', 
         '{"housePayment": "bank", "hotelMove": "not_allowed", "deckExhaustion": "reshuffle", "extraProperties": "cap", "buildingForfeiture": "keep_floating", "propertyMerging": "no_merge", "quadrupleRent": false, "forcedDealToDealBreaker": false, "justSayNoEmptyHand": true, "justSayNoOnZero": true}', 
         true, 0)
    """)


def downgrade():
    op.drop_table('user_configurations')
    op.drop_table('configuration_presets')