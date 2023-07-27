# This file is a wrapper for the Nostr Serverless API
import os
import requests


def post_to_endpoint(url, json_payload, headers=None):
	response = requests.post(url, json=json_payload, headers=headers)
	return response


def fetch_notes(base_url, filters, relays):
	url = base_url + "/v0/fetch/notes"
	json_payload = {
	 "relays": relays,
	 "authors": getattr(filters, 'authors', None),
	 "tags": getattr(filters, 'tags', None),
	 "event_refs": getattr(filters, 'event_refs', None),
	 "pubkey_refs": getattr(filters, 'pubkey_refs', None),
	 "since": getattr(filters, 'since', None),
	 "until": getattr(filters, 'until', None),
	 "limit": getattr(filters, 'limit', None)
	}
	response = post_to_endpoint(url, json_payload, headers={'Content-Type': 'application/json'})
	return response.json()

class Filter:
	pass

def download_unfiltered_nostr_data(n_samples):
    base_url = os.environ['BASE_URL']
    filters = Filter()
    filters.limit = n_samples
    relays = ['wss://relay.nostr.band']
    return fetch_notes(base_url, filters, relays)

def download_author_notes(author_pubkey, n_samples):
	base_url = os.environ['BASE_URL']
	filters = Filter()
	filters.limit = n_samples
	filters.authors = [author_pubkey]
	relays = ['wss://relay.nostr.band']
	return fetch_notes(base_url, filters, relays)