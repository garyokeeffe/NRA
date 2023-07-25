from nsa_wrapper import download_unfiltered_nostr_data
from openai_wrapper import embedding_annotate
from organization_helpers import save, load

'''
notes = download_unfiltered_nostr_data(1000)

save(notes, "notes")
#notes = load("notes")

notes_with_embeddings = embedding_annotate(notes)

save(notes_with_embeddings, "notes_with_embeddings")
'''
notes_with_embeddings = load("notes_with_embeddings")





