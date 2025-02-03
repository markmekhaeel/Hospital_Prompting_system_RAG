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
    return render_template('Policy-insert.html')

@app.route('/insert',methods=['POST'])
def insert():
    name= request.form.get('Name')
    policy = request.form.get('policy')
    address = request.form.get('add')
    landline = request.form.get('landline')
    open_date = request.form.get('open_date')

    
    db = sqlite3.connect('./data/Xyris.db')
    cursor = db.cursor()
    sql = f"INSERT INTO Policy (Name, 'Policy Description', Address, Landline, 'Open Date') VALUES ('{name}', '{policy}', '{address}', '{landline}', '{open_date}')"
    cursor.execute(sql)
    db.commit()
    db.close()

    #vector data
    df = pd.DataFrame([[name, policy, address, landline, open_date]])
    chunks, metadatas, ids = vectorize_data(df, 'Policy')

    #store vectors to database
    add_to_collection(collection,chunks,metadatas,ids)

    return 'added succesfully'
if __name__ == '__main__':
    app.run()