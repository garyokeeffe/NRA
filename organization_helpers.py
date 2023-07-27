import json
import numpy as np
from nsa_wrapper import download_author_notes
from openai_wrapper import embedding_annotate

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
    notes = download_author_notes(author_pubkey, 2)
    embedded_notes = embedding_annotate(notes)
    embeddings = get_embeddings_array(embedded_notes)
    return embeddings.mean(axis=0).tolist()

def filter_notes(notes):
