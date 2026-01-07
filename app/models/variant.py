from __future__ import annotations

from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from ..db.session import Base  # Corrected import for Base

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