import sqlite3
from flask import Flask, request, render_template
from utils.process_data import read_sql, vectorize_data, add_to_collection
from utils.rag import client
import pandas as pd

collection = client.get_collection('Hospital-data')

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def home():
    return render_template('Specialities-insert.html')

@app.route('/insert',methods=['POST'])
def insert():
    spec_name= request.form.get('spec')
    definition = request.form.get('def')

    
    db = sqlite3.connect('./data/Xyris.db')
    cursor = db.cursor()
    sql = f"INSERT INTO Specialities ('Speciality Name', Definition) VALUES ('{spec_name}', '{definition}')"
    cursor.execute(sql)
    db.commit()
    db.close()

    #vector data
    df = pd.DataFrame([[spec_name,definition]])
    chunks, metadatas, ids = vectorize_data(df, 'Specialities')

    #store vectors to database
    add_to_collection(collection,chunks,metadatas,ids)

    return 'added succesfully'

if __name__ == '__main__':
    app.run()