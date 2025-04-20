"""empty message

Revision ID: c0a169f5ca98
Revises: a307c8b37ecc
Create Date: 2025-04-20 16:33:52.107799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0a169f5ca98'
down_revision: Union[str, None] = 'a307c8b37ecc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
