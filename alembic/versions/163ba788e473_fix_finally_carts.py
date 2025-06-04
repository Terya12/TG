"""fix Finally_carts

Revision ID: 163ba788e473
Revises: afa071db458b
Create Date: 2025-06-04 12:31:00.985989

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "163ba788e473"
down_revision: Union[str, None] = "afa071db458b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        op.f("finally_carts_card_id_key"), "finally_carts", type_="unique"
    )


def downgrade() -> None:
    op.create_unique_constraint(
        op.f("finally_carts_card_id_key"),
        "finally_carts",
        ["card_id"],
        postgresql_nulls_not_distinct=False,
    )
