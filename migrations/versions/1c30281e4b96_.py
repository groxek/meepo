"""empty message

Revision ID: 1c30281e4b96
Revises: b1cc6253c9fb
Create Date: 2026-08-07 22:45:47.592210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c30281e4b96'
down_revision: Union[str, Sequence[str], None] = 'b1cc6253c9fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tasks', sa.Column('ege_number', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('tasks', 'ege_number')
