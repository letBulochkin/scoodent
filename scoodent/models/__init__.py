"""Scoodent models."""

from sqlalchemy import (
    Column, Date, DateTime, Table, ForeignKey, Integer, String, Text, Boolean
)
from sqlalchemy.orm import relationship

from scoodent.common.db import Base


actor_disk_table = Table(
    "actor_disk", Base.metadata,
    Column("actor_id", Integer, ForeignKey("actor.id")),
    Column("disk_id", Integer, ForeignKey("disk.id")))


genre_disk_table = Table(
    "genre_disk", Base.metadata,
    Column("genre_id", Integer, ForeignKey("genre.id")),
    Column("disk_id", Integer, ForeignKey("disk.id")))


class Actor(Base):

    __tablename__ = "actor"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Genre(Base):

    __tablename__ = "genre"

    id = Column(Integer, primary_key=True)
    film_genre = Column(String(255), nullable=False)


class Disk(Base):
    """model for disk instance"""

    __tablename__ = "disk"

    id = Column(Integer, primary_key=True)
    acq_date = Column(Date, nullable=False)
    title = Column(String(255), nullable=False)
    director = Column(String(255), nullable=False)
    year = Column(Integer)
    actors = relationship("Actor", secondary=actor_disk_table)
    genre = relationship("Genre", secondary=genre_disk_table)
    rating = Column(Integer)
    existance = Column(Boolean, nullable=False)


class Customer(Base):
    """model for customer instance"""

    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    phone_number = Column(String(32))
    name = Column(String(255), nullable=False)
    passport = Column(String(255), nullable=False)
    ordered = Column(Integer, default=0)


class Rental(Base):
    """model for disk rental instance"""

    __tablename__ = "rental"
    id = Column(Integer, primary_key=True)
    # if customer name is deleted, delete all his rents
    rent_customer = Column(
        Integer, ForeignKey("customer.id", ondelete="cascade"))
    customer = relationship("Customer")

    # if disk is deleted, do not delete any rents
    rent_disk = Column(Integer, ForeignKey("disk.id", ondelete="SET NULL"))
    disk = relationship("Disk")

    returned = Column(Boolean, default=False)
    time_taken = Column(DateTime)
    time_returned = Column(DateTime)
    deposit = Column(Integer)
