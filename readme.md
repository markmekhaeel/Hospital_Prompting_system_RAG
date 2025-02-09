# introduction to Prompting Hospital system
a system to process excel file containing of 5 sheets including information on 
physicians, schedules, and pricelists. The system will answer user inquiries using RAG, such as the schedule of a specific doctor, the most appropriate doctor or specialty based on the question, the price of a specific service, or retrieving metadata about the hospital. 

our system consist of streamlit app that connects to rag-API

# Get started:: requirements
all modules required are in requirements.txt
```
pandas
openpyxl
openai
flask
sqlite3
chromadb
streamlit
requests
```

# utils functions
```bash
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
│   │       Schedules-insert.html
│   │       Specialities-insert.html
│   │
│   └───utils
│       │   process_data.py
│       └───rag.py
│      
│
├───data
│       Xyris HIS_data.xlsx
└───────Xyris.db
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
2. get_context_combined(results): combine all results that matched the query
3. get_prompt(context, query): Generate a prompt combining context and query
4. generate_response(query, context): Generate a response using OpenAI
5. rag_query(collection, query, n_chunks = 2): Perform RAG query: retrieve relevant chunks and generate an answer


## How to run streamlit app
First, we use cd to change the directory to the project folder then run the main.py file to create a vector database
```bash
python3 main.p
```
Second, we run rag-API.py to start connecting to the vector database and connecting to ChatGPT 4o mini-chat
```bash
python3 API/rag-API.py
```
and then we run Streamlit app through terminal
```bash
streamlit run J:\..\Hospital_Prompting_system_RAG\Stream-app.py
```


## How to insert data into the database
there's an API for each table to insert data run the API for the table you want to add a record at and there's an HTML file to easily interface with the API at 127.0.0.1:5000
example: inserting data to physician table we run physician-API.py
```bash
python3 API/physician-API.py
```

```bash
python3 API/Schedules.py
```
