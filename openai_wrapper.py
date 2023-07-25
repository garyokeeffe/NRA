# This file is a wrapper for OpenAI
import openai


def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   text = text.encode('utf-8').decode('unicode_escape')
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

def embedding_annotate(notes):
    for note in notes:
        notes[note]['embedding'] = get_embedding(notes[note]['content'], model='text-embedding-ada-002')
    return notes