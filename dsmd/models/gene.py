from db import db

class Gene(db.Model):
    __tablename__ = 'gene'
    id = db.Column(db.Integer, primary_key=True)
    Gene_name = db.Column(db.String(50))
    Transcript_id = db.Column(db.String(50))

    def __init__(self, gene_name, transcript_id):
        self.Gene_name = gene_name
        self.Transcript_id = transcript_id

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_record(self):
        db.session.merge(self)
        db.session.flush()
        db.session.commit()
    
    def json(self):
        return {"Gene_name": self.Gene_name, "Transcript_id":self.Transcript_id}
    
    @classmethod
    def find_by_Gene_name(cls, gene_name):
        return cls.query.filter_by(Gene_name=gene_name).all()

    @classmethod
    def find_by_Transcript_id(cls, transcript_id):
        return cls.query.filter_by(Transcript_id=transcript_id).all()
    
    @classmethod
    def find_all(cls):
        return cls.query.order_by(Gene.Gene_name).all()
        
    @classmethod
    def find_by_Gene_char(cls, gene_char):
        return cls.query.filter(Gene.Gene_name.startswith(gene_char.upper())).all()