"""add content to posts table

Revision ID: adac6d309609
Revises: 4dfa64122323
Create Date: 2024-10-08 10:14:31.368062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adac6d309609'
down_revision: Union[str, None] = '4dfa64122323'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'column')
    pass
