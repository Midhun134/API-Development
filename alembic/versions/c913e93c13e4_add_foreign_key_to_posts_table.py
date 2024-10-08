"""add foreign-key to posts table

Revision ID: c913e93c13e4
Revises: 2a47c0d5f8a3
Create Date: 2024-10-08 10:59:11.961551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c913e93c13e4'
down_revision: Union[str, None] = '2a47c0d5f8a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='userss', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')

    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
