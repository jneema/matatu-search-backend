"""add_image_url_and_optional_coords

Revision ID: b23ae7199c0a
Revises: 0000_create_all_tables
Create Date: 2026-04-26 19:15:53.436645

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'b23ae7199c0a'
down_revision: Union[str, None] = '0000_create_all_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add image_url columns
    op.add_column('stages', sa.Column('image_url', sa.String(), nullable=True))
    op.add_column('saccos', sa.Column('image_url', sa.String(), nullable=True))

    op.alter_column('stages', 'latitude',
               existing_type=sa.Numeric(precision=10, scale=8),
               nullable=True)
    op.alter_column('stages', 'longitude',
               existing_type=sa.Numeric(precision=11, scale=8),
               nullable=True)

def downgrade() -> None:
    op.alter_column('stages', 'longitude',
               existing_type=sa.Numeric(precision=11, scale=8),
               nullable=False)
    op.alter_column('stages', 'latitude',
               existing_type=sa.Numeric(precision=10, scale=8),
               nullable=False)
    
    op.drop_column('saccos', 'image_url')
    op.drop_column('stages', 'image_url')
