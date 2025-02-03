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
    return render_template('Physicians-insert.html')

@app.route('/insert',methods=['POST'])
def insert():
    name= request.form.get('Name_col')
    speciality = request.form.get('Speciality_col')
    degree = request.form.get('Degree_col')

    
    db = sqlite3.connect('./data/Xyris.db')
    cursor = db.cursor()
    sql = f"INSERT INTO Physicians (Name, Speciality, Degree) VALUES ('{name}', '{speciality}', '{degree}')"
    cursor.execute(sql)
    db.commit()
    db.close()

    #vector data
    df = pd.DataFrame([[name, speciality, degree]])
    chunks, metadatas, ids = vectorize_data(df, 'Physicians')

    #store vectors to database
    add_to_collection(collection,chunks,metadatas,ids)
    

    return 'added succesfully'
if __name__ == '__main__':
    app.run()