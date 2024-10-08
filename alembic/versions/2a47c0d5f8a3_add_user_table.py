"""add user table

Revision ID: 2a47c0d5f8a3
Revises: adac6d309609
Create Date: 2024-10-08 10:24:31.314213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a47c0d5f8a3'
down_revision: Union[str, None] = 'adac6d309609'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('userss', sa.Column('id', sa.Integer(), nullable=False),sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('userss')
    pass
