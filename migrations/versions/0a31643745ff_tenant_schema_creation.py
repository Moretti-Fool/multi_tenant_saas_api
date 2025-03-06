"""Tenant Schema Creation

Revision ID: 0a31643745ff
Revises: 
Create Date: 2025-03-06 14:00:03.805722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a31643745ff'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS tenant")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS tenant CASCADE")
