from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session

from ..models import Gene as GeneORM
from ..schemas import GeneCreate
from .ucsc import get_gene_data

def get_or_fetch_gene(db: Session, symbol: str) -> GeneORM:
    """
    Retrieve gene from DB, fetch from UCSC if not found.
    If UCSC fails, return a placeholder gene instead of None.
    """
    sym_up = symbol.strip().upper()

    # 1️⃣ Check DB
    db_gene = db.query(GeneORM).filter(GeneORM.symbol == sym_up).first()
    if db_gene:
        return db_gene

    # 2️⃣ Try UCSC
    gene_create: Optional[GeneCreate] = get_gene_data(sym_up)

    # 3️⃣ If UCSC fails, return placeholder
    if not gene_create:
        print(f"[WARN] UCSC fetch failed for {sym_up}, returning placeholder")
        gene_create = GeneCreate(
            symbol=sym_up,
            name=sym_up,
            description="No data available",
            chromosome="NA",
            start_position=0,
            end_position=0,
            strand="+",
            gene_type="unknown",
            species="Homo sapiens",
        )

    # 4️⃣ Save to DB
    db_gene = GeneORM(**gene_create.model_dump())
    db.add(db_gene)
    db.commit()
    db.refresh(db_gene)

    return db_gene
