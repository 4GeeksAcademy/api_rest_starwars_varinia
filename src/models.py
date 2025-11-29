from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    personajes: Mapped[List["FavoritPeople"]] = relationship()
    planetas: Mapped[List["FavoritPlanet"]] = relationship()


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(40), nullable=False)
    species: Mapped[str] = mapped_column(String(60), nullable=False)
    personajes: Mapped[List["FavoritPeople"]] = relationship(back_populates="People")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "species": self.species,

        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    diameter: Mapped[int] = mapped_column(Numeric(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(100), nullable=False)
    population: Mapped[int] = mapped_column(Numeric(120), nullable=False)
    planet: Mapped[List["FavoritPlanet"]] = relationship(back_populates="Planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "orbital_period": self.orbital_period,
            "climate": self.climate,
            "population": self.population,
            # do not serialize the password, its a security breach
        }


class FavoritPeople(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_people: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    people: Mapped["People"] = relationship(back_populates="favoritpeople")



    def serialize(self):
        return {
            "name": self.name,
        }


class FavoritPlanet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    id_planet: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    planet: Mapped["Planet"] = relationship(back_populates="favoritplanet")

    def serialize(self):
        return {
         
            "name": self.name,
        }

