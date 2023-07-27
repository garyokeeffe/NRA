import json
import numpy as np
from api_wrappers.nsa_wrapper import download_author_notes
from api_wrappers.openai_wrapper import embedding_annotate
from helpers.text_helpers import tag_media_notes, tag_nostr_notes


def save(data_object, name):
    with open(f'{name}.json', 'w') as f:
        json.dump(data_object, f)

def load(name):
    with open(f'{name}.json', 'r') as f:
        return json.load(f)
    

def get_embeddings_array(notes_with_embeddings):
    embeddings = [note['embedding'] for note in notes_with_embeddings.values()]
    return np.array(embeddings)

def initial_semantic_focus(author_pubkey):
    notes = download_author_notes(author_pubkey, 20)
    tag_media_notes(notes)
    tag_nostr_notes(notes)
    embedded_notes = embedding_annotate(notes)
    embeddings = get_embeddings_array(embedded_notes)
    return embeddings.mean(axis=0).tolist()


