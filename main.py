from api_wrappers.nsa_wrapper import download_unfiltered_nostr_data
from api_wrappers.openai_wrapper import embedding_annotate
from helpers.text_helpers import print_formatted_query_result, tag_media_notes, tag_nostr_notes, filter_long_and_short_notes
from helpers.misc_helpers import save, load, initial_semantic_focus
from api_wrappers.chromadb_wrapper import set_up_database, upload_embeddings_to_database, get_random_note


# Step 1: Fetch Data from Nostr
notes = download_unfiltered_nostr_data(3000)
save(notes, "notes")
#notes = load("notes")


#Step 2: Map data to Embeddings
tag_media_notes(notes)
tag_nostr_notes(notes)
filter_long_and_short_notes(notes)
notes_with_embeddings = embedding_annotate(notes)
save(notes_with_embeddings, "notes_with_embeddings")
#notes_with_embeddings = load("notes_with_embeddings")


# Step 3: Send Data To Database
database = set_up_database()
upload_embeddings_to_database(database, notes_with_embeddings)


# Step 4: Make Initial Guess
semantic_focus = initial_semantic_focus('npub10mgeum509kmlayzuvxhkl337zuh4x2knre8ak2uqhpcra80jdttqqvehf6')

# Step 5: Get feedback and guess again
while True:
	query_result = get_random_note(database,semantic_focus)
	
	print_formatted_query_result(query_result)

	response = input("Enter 'y' if you like this note or 'n' if not (or 'exit' to stop): ")
	if response.lower() == 'exit':
		break
	if response.lower() == 'y':
		semantic_focus  = [.9*x + .1*y  for x, y in zip(semantic_focus, query_result['embeddings'])]
	if response.lower() == 'n':
		semantic_focus  = [1.1*x + -.1*y  for x, y in zip(semantic_focus, query_result['embeddings'])]
