"""Utility script to create database tables."""

from . import Base, engine

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
