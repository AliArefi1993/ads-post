"""Create add relation user and ads

Revision ID: 287b495c9970
Revises: 39c6eccc0d07
Create Date: 2023-09-17 23:51:45.299549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '287b495c9970'
down_revision: Union[str, None] = '39c6eccc0d07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ads', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'ads', 'user', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ads', type_='foreignkey')
    op.drop_column('ads', 'owner_id')
    # ### end Alembic commands ###
