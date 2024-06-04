"""UltimaMigracionActual

Revision ID: 4907341dcddc
Revises: 5a39e26833ad
Create Date: 2024-06-04 21:17:02.769398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4907341dcddc'
down_revision: Union[str, None] = '5a39e26833ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
