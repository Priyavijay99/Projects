# import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine("mysql://root:1234@localhost:3306/dsmd",echo = True)
from sqlalchemy import Table, Column, Integer, String, MetaData
meta = MetaData()

students = Table(
   'gene', meta, 
   Column('Gene_name', String(250)), 
   Column('Transcript_id', String(250)) 
)
# meta.create_all(engine)


df = pd.read_json('data.json',typ='series')
conn=engine.connect()
# for gene,transcript in df.iteritems():
# 	obj=students.insert().values(Gene_name=gene,Transcript_id=transcript)
# 	result=conn.execute(obj)
# print(result)
# print(df)



	