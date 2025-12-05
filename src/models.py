from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(400), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorite_planets: Mapped[List["FavoritePlanets"]] = relationship(back_populates="user")
    favorite_people: Mapped[List["FavoritePeople"]] = relationship(back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(40), nullable=False)
    species: Mapped[str] = mapped_column(String(60), nullable=False)
    favs: Mapped[List["FavoritePeople"]] = relationship(back_populates="people")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "species": self.species,

        }


class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    diameter: Mapped[int] = mapped_column(Numeric(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(100), nullable=False)
    population: Mapped[int] = mapped_column(Numeric(120), nullable=False)
    favs: Mapped[List["FavoritePlanets"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "population": self.population,
        }


class FavoritePeople(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    people: Mapped["People"] = relationship(back_populates="favs")
    user: Mapped["User"] = relationship(back_populates="favorite_people")



    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people": self.people.serialize(),
        }


class FavoritePlanets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=True)
    planet: Mapped["Planets"] = relationship(back_populates="favs")
    user: Mapped["User"] = relationship(back_populates="favorite_planets")

    def serialize(self):
        return {
         
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize(),
        }

