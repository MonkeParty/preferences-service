"""Create user_info table

Revision ID: f05303628cb4
Revises: 6914bf7ab3fa
Create Date: 2024-12-08 22:44:17.620620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f05303628cb4'
down_revision: Union[str, None] = '6914bf7ab3fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_info',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('avg_rating', sa.Float(), nullable=False),
    sa.Column('genres_preference', sa.JSON(), nullable=False),
    sa.Column('tags_preference', sa.JSON(), nullable=False),
    sa.Column('svd_vector', sa.ARRAY(sa.Float()), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_user_info_user_id'), 'user_info', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_info_user_id'), table_name='user_info')
    op.drop_table('user_info')
    # ### end Alembic commands ###
