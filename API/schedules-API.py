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
    return render_template('Schedules-insert.html')

@app.route('/insert',methods=['POST'])
def insert():
    name= request.form.get('Name_col')
    Monday = request.form.get('Monday')
    Tuesday = request.form.get('Tuesday')
    Wednesday= request.form.get('Wednesday')
    Thursday = request.form.get('Thursday')
    Friday = request.form.get('Friday')
    Saturday= request.form.get('Saturday')
    Sunday = request.form.get('Sunday')

    
    db = sqlite3.connect('./data/Xyris.db')
    cursor = db.cursor()
    sql = f"INSERT INTO Schedules (Name, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) VALUES ('{name}', '{Monday}', '{Tuesday}','{Wednesday}', '{Thursday}', '{Friday}','{Saturday}', '{Sunday}')"
    cursor.execute(sql)
    db.commit()
    db.close()

    #vector data
    df = pd.DataFrame([[name, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]])
    chunks, metadatas, ids = vectorize_data(df, 'Schedules')

    #store vectors to database
    add_to_collection(collection,chunks,metadatas,ids)

    return 'added succesfully'
if __name__ == '__main__':
    app.run()