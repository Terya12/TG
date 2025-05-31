"""Initial migration

Revision ID: afa071db458b
Revises:
Create Date: 2025-05-31 16:39:29.745042

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "afa071db458b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("category_name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("category_name"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("telegram", sa.BigInteger(), nullable=False),
        sa.Column("phone", sa.String(length=30), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("telegram"),
    )
    op.create_table(
        "carts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("total_price", sa.DECIMAL(precision=12, scale=2), nullable=False),
        sa.Column("total_product", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("image", sa.String(length=100), nullable=False),
        sa.Column("price", sa.DECIMAL(precision=12, scale=2), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("product_name"),
    )
    op.create_table(
        "finally_carts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_name", sa.String(length=50), nullable=False),
        sa.Column("finally_price", sa.DECIMAL(precision=12, scale=2), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("card_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["card_id"], ["carts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("card_id"),
        sa.UniqueConstraint("card_id", "product_name"),
    )


def downgrade() -> None:
    op.drop_table("finally_carts")
    op.drop_table("products")
    op.drop_table("carts")
    op.drop_table("users")
    op.drop_table("categories")
