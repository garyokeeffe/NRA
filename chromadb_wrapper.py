import chromadb
from openai_wrapper import get_embedding

def set_up_database():
    client = chromadb.Client()
    return client.create_collection("nostr_data")

def upload_embeddings_to_database(database, notes_with_embeddings):
    for note in notes_with_embeddings:
        database.add(
            documents = [notes_with_embeddings[note]['content']],
            metadatas=[{
	                'author': notes_with_embeddings[note]['author'],
	                'time_created': notes_with_embeddings[note]['time_created']
	                }],
            ids=[note], 
            embeddings = notes_with_embeddings[note]['embedding']
        )
    return database
   

def query_database_embedding(database, embedding, n_results = 5):
    return database.query(
        query_embeddings=[embedding],
        n_results=n_results,
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    )

def query_database_string(database, text, n_results = 5):
    embedding = get_embedding(text)
    return query_database_embedding(database, embedding, n_results)