"""remove date col from Reading table

Revision ID: 5779ec187c8e
Revises: e8fa8dad1a57
Create Date: 2024-10-20 16:54:36.435378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '5779ec187c8e'
down_revision: Union[str, None] = 'e8fa8dad1a57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
