"""Add Telomere model

Revision ID: a79e5f6d975d
Revises: e35140c3bd07
Create Date: 2026-01-05 10:43:47.413062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a79e5f6d975d'
down_revision: Union[str, Sequence[str], None] = 'e35140c3bd07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
