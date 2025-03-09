"""Tenant Schema Creation

Revision ID: 69d73a455a8d
Revises: 
Create Date: 2025-03-09 16:37:10.768473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69d73a455a8d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS tenant")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS tenant CASCADE")