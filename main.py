import pandas as pd
import os
import sqlite3
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

from api.utils.process_data import *
from api.utils.rag import *

filepath = 'data/Xyris HIS_data.xlsx'
database = 'data/Xyris.db'

tables = excel_to_db(filepath, database)


#prepare vector database

sentence_transformer = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L12-V2') 


collection = client.get_or_create_collection(name= 'Hospital-data')

#process excel sheet
chunks, metadatas, ids= process_excel(collection,tables, database)



query = 'what is Dr. Alice\'s schedules'
response = rag_query(collection, query)

print(response)






  