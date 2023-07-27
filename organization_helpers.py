import json
import numpy as np
from nsa_wrapper import download_author_notes
from openai_wrapper import embedding_annotate
import re


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


def filter_long_and_short_notes(notes):
    max_text_length = 1000
    min_text_length = 20
    keys_to_delete = [k for k, v in notes.items() if len(v['content']) > max_text_length]
    for key in keys_to_delete:
        del notes[key]
    keys_to_delete = [k for k, v in notes.items() if len(v['content']) < min_text_length]
    for key in keys_to_delete:
        del notes[key]
    return notes



def tag_media_notes(notes):
    media_types = [".gif", "https", "youtube.com", ".png", ".jpg", ".webp", "spotify", ".mov"]

    url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    for k, v in notes.items():
        urls = re.findall(url_pattern, v['content'])
        for url in urls:
            if any(type in url[0] for type in media_types):
                v['content'] = v['content'].replace(url[0], ' [media_object] ')

    return notes

def tag_nostr_notes(notes):
    media_types = ["nostr:"]

    for k, v in notes.items():
        for media_type in media_types:
            pattern = re.escape(media_type) + r'\S*'
            v['content'] = re.sub(pattern, '[nostr_object]', v['content'])

    return notes

def print_formatted_query_result(query_result):
	print("-" * 50)
	print('Nostr Note: ' + query_result['ids'])
	print('Author: ' + query_result['metadatas']['author'])
	print("-" * 50)
	print(query_result['documents'])
	print("-" * 50)