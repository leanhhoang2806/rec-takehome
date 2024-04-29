"""create_tables

Revision ID: 0214473ff4a2
Revises: 
Create Date: 2024-04-27 02:07:37.509851

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "0214473ff4a2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.create_table(
        "Eaters",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
            primary_key=True,
        ),
        sa.Column("name", sa.String, nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )

    op.create_table(
        "Dietary_Restrictions",
        sa.Column(
            "eater_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("Eaters.id"),
            nullable=False,
        ),
        sa.Column("diet_name", sa.String, nullable=False),
    )

    op.create_table(
        "Restaurants",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("name", sa.String, nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
            onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    op.create_table(
        "Endorsements",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("endorsement", sa.String, nullable=False),
    )

    op.create_table(
        "Restaurant_Endorsements",
        sa.Column(
            "restaurant_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("Restaurants.id"),
            primary_key=True,
        ),
        sa.Column(
            "endorsement_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("Endorsements.id"),
            primary_key=True,
        ),
    )

    op.create_table(
        "Restaurant_Available_Table",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "restaurant_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("Restaurants.id"),
            nullable=False,
        ),
        sa.Column(
            "two_people_table", sa.Integer, nullable=False, server_default=sa.text("0")
        ),
        sa.Column(
            "four_people_table", sa.Integer, nullable=False, server_default=sa.text("0")
        ),
        sa.Column(
            "six_people_table", sa.Integer, nullable=False, server_default=sa.text("0")
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )

    op.create_check_constraint(
        "chk_two_positive",
        "Restaurant_Available_Table",
        sa.text("two_people_table >= 0"),
    )
    op.create_check_constraint(
        "chk_four_positive",
        "Restaurant_Available_Table",
        sa.text("four_people_table >= 0"),
    )
    op.create_check_constraint(
        "chk_six_positive",
        "Restaurant_Available_Table",
        sa.text("six_people_table >= 0"),
    )

    op.create_table(
        "Reservations",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
            primary_key=True,
        ),
        sa.Column(
            "restaurant_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("Restaurants.id"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )

    op.create_table(
        "Reservation_Eater",
        sa.Column(
            "reservation_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("Reservations.id"),
            primary_key=True,
        ),
        sa.Column(
            "eater_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("Eaters.id"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("Eaters")
    op.drop_table("Restaurants")
    op.drop_table("Endorsements")
    op.drop_table("Restaurant_Endorsements")
    op.drop_table("Restaurant_Available_Table")
    op.drop_table("Reservations")
    op.drop_table("Reservation_Eater")
    op.drop_table("Dietary_Restrictions")
    op.drop_constraint("chk_two_positive", "Restaurant_Available_Table", type_="check")
    op.drop_constraint("chk_four_positive", "Restaurant_Available_Table", type_="check")
    op.drop_constraint("chk_six_positive", "Restaurant_Available_Table", type_="check")
