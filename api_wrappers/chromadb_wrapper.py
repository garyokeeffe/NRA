import chromadb
from api_wrappers.openai_wrapper import get_embedding
import random


def set_up_database():
    client = chromadb.Client()
    return client.create_collection("nostr_test")

def upload_embeddings_to_database(database, notes_with_embeddings):
    for note in notes_with_embeddings:
        database.add(
            documents = [notes_with_embeddings[note]['content']],
            metadatas=[{
	                'author': notes_with_embeddings[note]['author'],
	                'time_created': notes_with_embeddings[note]['time_created']
	                }],
            ids=[note], 
            embeddings = [notes_with_embeddings[note]['embedding']]
        )
    return database
   

def query_database_embedding(database, embedding, n_results = 5):
    return database.query(
        query_embeddings=[embedding],
        n_results=n_results, include=['embeddings', 'distances', 'documents', 'metadatas']
    )

def query_database_string(database, text, n_results = 5):
    embedding = get_embedding(text)
    return query_database_embedding(database, embedding, n_results)

def get_random_note(database, semantic_focus, n_options = 10):
    list_of_results = query_database_embedding(database, semantic_focus, n_options)
    min_size = min(len(v[0]) for v in list_of_results.values() if v is not None)
    random_choice = random.randint(0, min_size-1)
    return {k: v[0][random_choice] if v is not None else v for k, v in list_of_results.items()}
