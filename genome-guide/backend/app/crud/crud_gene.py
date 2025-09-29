from sqlalchemy.orm import Session, joinedload
from ..models import gene as model_gene

def get_gene_by_name(db: Session, gene_name: str):
    """
    Retrieve a single gene by its exact name, and also load its related chromosome data.
    """
    return db.query(model_gene.Gene).options(joinedload(model_gene.Gene.chromosome)).filter(model_gene.Gene.gene_name == gene_name).first()

def search_genes_by_name(db: Session, query: str, limit: int = 10):
    """
    Search for genes and also load their related chromosome data.
    """
    return db.query(model_gene.Gene).options(joinedload(model_gene.Gene.chromosome)).filter(model_gene.Gene.gene_name.ilike(f"%{query}%")).limit(limit).all()