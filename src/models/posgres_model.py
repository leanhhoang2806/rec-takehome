# coding: utf-8
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

Base = declarative_base()
metadata = Base.metadata


class Eater(Base):
    __tablename__ = "Eaters"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String, nullable=False)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    reservations = relationship("Reservation", secondary="Reservation_Eater")


class Endorsement(Base):
    __tablename__ = "Endorsements"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    endorsement = Column(String, nullable=False)

    restaurants = relationship("Restaurant", secondary="Restaurant_Endorsements")


class Restaurant(Base):
    __tablename__ = "Restaurants"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String, nullable=False)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


t_Dietary_Restrictions = Table(
    "Dietary_Restrictions",
    metadata,
    Column("eater_id", ForeignKey("Eaters.id"), nullable=False),
    Column("diet_name", String, nullable=False),
)


class Reservation(Base):
    __tablename__ = "Reservations"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    restaurant_id = Column(ForeignKey("Restaurants.id"), nullable=False)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    restaurant = relationship("Restaurant")


class RestaurantAvailableTable(Base):
    __tablename__ = "Restaurant_Available_Table"
    __table_args__ = (
        CheckConstraint("four_people_table >= 0"),
        CheckConstraint("six_people_table >= 0"),
        CheckConstraint("two_people_table >= 0"),
    )

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    restaurant_id = Column(ForeignKey("Restaurants.id"), nullable=False)
    two_people_table = Column(Integer, nullable=False, server_default=text("0"))
    four_people_table = Column(Integer, nullable=False, server_default=text("0"))
    six_people_table = Column(Integer, nullable=False, server_default=text("0"))
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    restaurant = relationship("Restaurant")


t_Restaurant_Endorsements = Table(
    "Restaurant_Endorsements",
    metadata,
    Column(
        "restaurant_id", ForeignKey("Restaurants.id"), primary_key=True, nullable=False
    ),
    Column(
        "endorsement_id",
        ForeignKey("Endorsements.id"),
        primary_key=True,
        nullable=False,
    ),
)


t_Reservation_Eater = Table(
    "Reservation_Eater",
    metadata,
    Column(
        "reservation_id",
        ForeignKey("Reservations.id"),
        primary_key=True,
        nullable=False,
    ),
    Column("eater_id", ForeignKey("Eaters.id"), primary_key=True, nullable=False),
)


RestaurantPydantic = sqlalchemy_to_pydantic(Restaurant)
ReservationPydantic = sqlalchemy_to_pydantic(Reservation)
