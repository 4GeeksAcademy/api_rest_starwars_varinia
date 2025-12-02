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
    planetas: Mapped[list["FavoritPlanets"]] = relationship(back_populates="user")
    personajes: Mapped[list["FavoritPeople"]] = relationship(back_populates="user")


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
    personajes: Mapped[list["FavoritPeople"]] = relationship(back_populates="people")

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
    planets: Mapped[List["FavoritPlanets"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "orbital_period": self.orbital_period,
            "climate": self.climate,
            "population": self.population,
        }


class FavoritPeople(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_people: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    people: Mapped["People"] = relationship(back_populates="personajes")
    user: Mapped["User"] = relationship(back_populates="personajes")



    def serialize(self):
        return {
            "name": self.name,
        }


class FavoritPlanets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    id_planet: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=True)
    planet: Mapped["Planets"] = relationship(back_populates="planets")
    user: Mapped["User"] = relationship(back_populates="planetas")

    def serialize(self):
        return {
         
            "name": self.name,
        }

