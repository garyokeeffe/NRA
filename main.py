from nsa_wrapper import download_unfiltered_nostr_data
from openai_wrapper import embedding_annotate
from organization_helpers import save, load
from chromadb_wrapper import set_up_database, upload_embeddings_to_database, query_database_string

'''
notes = download_unfiltered_nostr_data(1000)

save(notes, "notes")
#notes = load("notes")

notes_with_embeddings = embedding_annotate(notes)

save(notes_with_embeddings, "notes_with_embeddings")
'''
notes_with_embeddings = load("notes_with_embeddings")

database = set_up_database()

database = upload_embeddings_to_database(database, notes_with_embeddings)

semantic_focus = initial_semantic_focus('npub10mgeum509kmlayzuvxhkl337zuh4x2knre8ak2uqhpcra80jdttqqvehf6')
query_result = query_database_embedding(database, semantic_focus,n_results=10)
print(query_result['documents'])
'''
while True:
	query_text = input("Enter your nostr text query (or 'exit' to stop): ")
	if query_text.lower() == 'exit':
		break

	query_result = query_database_string(database, query_text)
	print(query_result['documents'])

