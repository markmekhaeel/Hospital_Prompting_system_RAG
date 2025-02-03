from flask import Flask, request, render_template, jsonify
from utils.rag import *

collection = client.get_collection('Hospital-data')


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('rag-home.html')

@app.route('/rag',methods=['POST'])
def rag():
    prompt = request.json['query']
    print('query recieved')
    response = rag_query(collection, prompt, 3)
    return jsonify({'answer': response}), 200


if __name__ == '__main__':
    app.run()