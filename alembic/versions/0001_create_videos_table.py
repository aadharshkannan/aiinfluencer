"""create videos table

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'videos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('proverb', sa.String(), nullable=False),
        sa.Column('story', sa.Text(), nullable=True),
        sa.Column('screenplay', sa.Text(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('videos')
