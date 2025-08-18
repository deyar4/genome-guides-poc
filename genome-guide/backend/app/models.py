from __future__ import annotations

from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Gene(Base):
    __tablename__ = "genes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default="")
    chromosome: Mapped[str] = mapped_column(String(10))
    start_position: Mapped[int] = mapped_column(Integer)
    end_position: Mapped[int] = mapped_column(Integer)
    strand: Mapped[str] = mapped_column(String(1))
    gene_type: Mapped[str] = mapped_column(String(50), default="protein_coding")
    species: Mapped[str] = mapped_column(String(50), default="Homo sapiens")

    def __repr__(self) -> str:
        return f"<Gene {self.symbol}>"

class Variant(Base):
    __tablename__ = "variants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rsid: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    chromosome: Mapped[str] = mapped_column(String(10))
    position: Mapped[int] = mapped_column(Integer)
    reference: Mapped[str] = mapped_column(String(255))
    alternate: Mapped[str] = mapped_column(String(255))
    gene_symbol: Mapped[str] = mapped_column(String(50))
    clinical_significance: Mapped[str] = mapped_column(String(255), default="")

    def __repr__(self) -> str:
        return f"<Variant {self.rsid}>"