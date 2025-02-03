# introduction to Prompting Hospital system
a system to process excel file containing of 5 sheets including information on 
physicians, schedules, and pricelists. The system's role will be to answer user inquiries using RAG, such as the schedule of a specific doctor, the most appropriate doctor or specialty based on the question, the price of a specific service, or retrieving metadata about the hospital. 

our system consist of streamlit app that connects to rag-API

# Get started :: requirements
all modules required are in requirements.txt
```
pandas
openpyxl
openai
flask
sqlite3
os
chromadb
streamlit
requests
```

# utils functions
```bash
│
├───API
│   │   physician-API.py
│   │   policy-API.py
│   │   pricelist-API.py
│   │   rag-API.py
│   │   schedules-API.py
│   │   specialities-API.py
│   │
│   ├───templates
│   │       Physicians-insert.html
│   │       Policy-insert.html
│   │       Pricelist-insert.html
│   │       rag-home.html
│   │       Schedules-insert.html
│   │       Specialities-insert.html
│   │
│   └───utils
│       │   process_data.py
│       │   rag.py
│       │
│       └───__pycache__
│               process_data.cpython-312.pyc
│               process_data.cpython-313.pyc
│               rag.cpython-313.pyc
│               __init__.cpython-313.pyc
│
├───chroma
│   │   chroma.sqlite3
│   │
│   └───95196828-3b20-4b76-b0b0-17ce39a48d9d
│           data_level0.bin
│           header.bin
│           length.bin
│           link_lists.bin
│
├───data
│       Xyris HIS_data.xlsx
│       Xyris.db
```
there's 2 scripts in utils folder in the API folder (to make it accessible for APIs)
### first one:: process_data.py
1. excel_to_db( filepath , database_name): load excel data from filepath and insert it to database_name  
  filepath: file path of data  
  database_name: dir of database to create/connect  
  returns Excel tables  
2. read_sql(query, database_name): execute sql query and return dataframe  
  db_table: database table  
  database: database engine  
returns dataframe
3. vectorize_data(df, table_name): retrieve data from database and vector it  
  database_name: database  
  table_name: retrieved table  
returns 3 variables (lists)
4. add_to_collection(collection, chunks, metadatas, ids):add vector data to vector database  
  collection: vector database  
  chunks: vector data  
  metadatas: sources of data  
  ids: ids of data  
5. process_excel(collection, tables, database_name): process excel file to extract all tables inside and vector it also store it to vector database
collection: vector database  
metadatas: sources of data  
ids: ids of data

### second file:: RAG.py
1. semantic_search(collection, query, k): search of semantic words in vector database that match query in (k) documents  
  collection: vector database  
  query: user's prompt  
  k: number of documents to retrieve from
2. get_context_combined(results): combine all results that matched query
3. get_prompt(context, query): Generate a prompt combining context and query
4. generate_response(query, context): Generate a response using OpenAI
5. rag_query(collection, query, n_chunks = 2): Perform RAG query: retrieve relevant chunks and generate answer


## How to run streamlit app
first we use cd to project folder then we run python by inserting in terminal
```bash
python3 API/rag-API.py
```
and then we run streamlit app through terminal
```bash
streamlit run J:\..\Hospital_Prompting_system_RAG\Stream-app.py
```


## how to insert data to database
there's API for each table to insert data run the API for the table you want to add record at and there's a html file to easy interface with the API in 127.0.0.1:5000

```bash
python3 API/Schedules.py
```