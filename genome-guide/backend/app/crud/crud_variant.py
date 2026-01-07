from sqlalchemy.orm import Session
from ..models.variant import Variant
from ..schemas.variant import VariantCreate

def get_variant_by_rsid(db: Session, rsid: str):
    return db.query(Variant).filter(Variant.rsid == rsid).first()

def get_variants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Variant).offset(skip).limit(limit).all()

def create_variant(db: Session, variant: VariantCreate):
    db_variant = Variant(
        rsid=variant.rsid,
        chromosome=variant.chromosome,
        position=variant.position,
        reference=variant.reference,
        alternate=variant.alternate,
        gene_symbol=variant.gene_symbol,
        clinical_significance=variant.clinical_significance
    )
    db.add(db_variant)
    db.commit()
    db.refresh(db_variant)
    return db_variant