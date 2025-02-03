import pandas as pd
import sqlite3

def excel_to_db(filepath: str,database_name: str):
  '''load excel data from filepath and insert it to database_name
  filepath: file path of data
  database_name: dir of database
  returns Excel tables'''

  #load excel file
  tables = pd.ExcelFile(filepath)

  #connect/create database_name
  db = sqlite3.connect(database_name)


  #insert data to sql database
  for sheet in tables.sheet_names:
    df = pd.read_excel(tables, sheet)
    df.to_sql(sheet, db,index=False, if_exists='replace')
  
  #end connection to database
  db.close()
  return tables


def read_sql(db_table, database_name):
  '''execute sql query and return dataframe
  db_table: database table
  database: database engine'''

  df = pd.read_sql(f'SELECT * FROM {db_table};',database_name)
  return df

def vectorize_data(df,table_name):
  '''retrieve data from database and vectorize it
  database_name: database
  table_name: retrieved table'''

  chunks= []
  metadatas = []
  ids = []
  for idx, row in df.iterrows():
    sentence = ''
    for col in df.columns:
      sentence += f'{col}: {row[col]}, \n'
    chunks.append(sentence)
    metadatas.append({'Source':table_name, 'index' : idx })
    ids.append(f'__{table_name}__{idx}')
  return chunks, metadatas, ids

def add_to_collection(collection, chunks, metadatas, ids):
  '''add vector data to vector database
  collection: vector database
  chunks: vector data
  metadatas: sources of data
  ids: ids of data'''

  collection.add(
      documents= chunks,
      metadatas= metadatas,
      ids= ids
  )

def process_excel(collection, tables, database_name):
  '''process excel file to extract all tables inside and vector it also store it to vector database'''
  
  db = sqlite3.connect(database_name)
  chunks=[]
  for sheet in tables.sheet_names:
    df = read_sql(sheet, db)
    #vector data
    print(f'Preparing vectors for sheet: {sheet}')
    chunks , metadatas, ids = vectorize_data(df,sheet)
    print(f'Number of chunks {len(chunks)} vectorized')
    print('adding to collection...')
    # add it to vector database
    add_to_collection(collection, chunks, metadatas, ids)
    print('added successfully')
  db.close()
  return chunks, metadatas, ids

