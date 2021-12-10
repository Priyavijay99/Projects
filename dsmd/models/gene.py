from db import db

class Gene(db.Model):
    __tablename__ = 'gene'
    id = db.Column(db.Integer, primary_key=True)
    Gene_name = db.Column(db.String(50))
    Transcript_id = db.Column(db.String(50))

    def __init__(self, gene_name, transcript_id):
        self.Gene_name = gene_name
        self.Transcript_id = transcript_id

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def json(self):
        return {"Gene_name": self.Gene_name, "Transcript_id":self.Transcript_id}
    
    @classmethod
    def find_all(cls):
        return cls.query.order_by(Gene.Gene_name).all()
        
    @classmethod
    def find_by_Gene_char(cls, gene_char):
        return cls.query.filter(Gene.Gene_name.startswith(gene_char.upper())).all()