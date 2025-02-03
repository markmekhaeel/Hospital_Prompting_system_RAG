from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions 
import os

client = chromadb.PersistentClient('chroma')


os.environ['OPENAI_API_KEY'] = 'OPENAI_API_KEY'
client_AI = OpenAI()



def semantic_search(collection, query, k):
  '''search of semantic words in vector database that match query in (k) documents 
  collection: vector database
  query: user's prompt
  k: number of documents to search in'''

  results= collection.query(query_texts= [query], n_results= k)

  return results


def get_context_combined(results):
    '''combine all results that matched query'''

    # Combine document chunks into a single context
    context = "\n\n".join(results['documents'][0])

    return context


def get_prompt(context, query):
    '''Generate a prompt combining context and query'''

    prompt = f'''Based on the following context and conversation history, 
    please provide a relevant and contextual response. If the answer cannot 
    be derived from the context, only use the conversation history or say 
    "I cannot answer this based on the provided information."

    Context from documents:
    {context}

    Human: {query}

    Assistant:'''

    return prompt

def generate_response(query, context):
    '''Generate a response using OpenAI'''
    prompt = get_prompt(context, query)


    response = client_AI.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,  # Lower temperature for more focused responses
        max_tokens=500
    )
    return response.choices[0].message.content


def rag_query(collection, query, n_chunks = 2):
    '''Perform RAG query: retrieve relevant chunks and generate answer'''
    # Get relevant chunks
    results = semantic_search(collection, query, n_chunks)
    context = get_context_combined(results)

    # Generate response
    response = generate_response(query, context)

    return response


