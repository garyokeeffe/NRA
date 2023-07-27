import json
import numpy as np
from api_wrappers.nsa_wrapper import download_author_notes
from api_wrappers.openai_wrapper import embedding_annotate
import re

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


def generate_formatted_query_result(query_result):
    result_str = "-" * 50
    result_str += '\nNostr Note: https://primal.net/e/' + query_result['ids']
    result_str += '\nAuthor: ' + query_result['metadatas']['author']
    result_str += '\n' + "-" * 50
    result_str += '\n' + query_result['documents']
    result_str += '\n' + "-" * 50
    return result_str

def print_formatted_query_result(query_result):
	print(generate_formatted_query_result(query_result))
        

def generate_formatted_query_object(query_result):
    result_dict = {
        'link': "https://primal.net/e/" + query_result['ids'],
        'author': query_result['metadatas']['author'],
        'documents': query_result['documents']
    }
    return result_dict
