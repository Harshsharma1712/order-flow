"""rename_cancelled_enum_value

Revision ID: 1d415e894964
Revises: 16a2591e1e94
Create Date: 2025-12-22 15:30:53.044578

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d415e894964'
down_revision: Union[str, Sequence[str], None] = '16a2591e1e94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE itemstatus RENAME VALUE 'cancelled' TO 'CANCELLED'")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TYPE itemstatus RENAME VALUE 'CANCELLED' TO 'cancelled'")
