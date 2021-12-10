import json
import pandas as pd
from flask import Flask, request, url_for, render_template, session, redirect, Response
from models.gene import Gene

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1117@127.0.0.1:3306/dsmd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'priyanka'

#CONSTANTS
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin"
USER = "user"
PASSWORD = "user"
INVOICE_NO = ""


def loadData():
    df = pd.read_json('data.json',typ='series')
    for gene_name,transcript_id in df.iteritems():
        gene = Gene(gene_name=gene_name, transcript_id=transcript_id)
        gene.insert_to_db()
    
@app.before_first_request
def create_tables():
    db.create_all()
    # loadData()

def getGeneByChar(char):
    return Gene.find_by_Gene_char(char)

@app.route('/', methods=['GET'])
def index():
    genes_by_char =getGeneByChar('A')
    gene_dicts_by_char = [gene.json() for gene in genes_by_char]
    gene_list = [gene.Gene_name for gene in Gene.find_all()]
    return render_template('geneSearch.html', all_gene_dicts=gene_dicts_by_char, tags=gene_list)

@app.route('/home/<char>', methods=['GET','POST'])
def delete(char):
    print("char to be shown:", char)
    genes_by_char =getGeneByChar(char)
    gene_dicts_by_char = [gene.json() for gene in genes_by_char]
    gene_list = [gene.Gene_name for gene in Gene.find_all()]
    return render_template('geneSearch.html', all_gene_dicts=gene_dicts_by_char, char=char, tags=gene_list)

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='127.0.0.1', port=80, debug=True)
