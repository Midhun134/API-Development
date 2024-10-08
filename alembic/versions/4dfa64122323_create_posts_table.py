"""create posts table

Revision ID: 4dfa64122323
Revises: 
Create Date: 2024-10-08 09:54:40.601474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4dfa64122323'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key = True), sa.Column('title', sa.String(), nullable=False))
    #in here we r creating a posts table using alembic
    pass


def downgrade() -> None:
    pass
