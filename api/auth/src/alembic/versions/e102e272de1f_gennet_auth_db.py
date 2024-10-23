"""gennet_auth_db

Revision ID: e102e272de1f
Revises: be8f09cba907
Create Date: 2024-05-19 11:03:19.922944

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = "e102e272de1f"
down_revision = "be8f09cba907"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column("first_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.add_column(
        "user",
        sa.Column("last_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.drop_column("user", "full_name")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("full_name", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.drop_column("user", "last_name")
    op.drop_column("user", "first_name")
    # ### end Alembic commands ###
