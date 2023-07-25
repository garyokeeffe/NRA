from nsa_wrapper import download_unfiltered_nostr_data
from organization_helpers import save, load

notes = download_unfiltered_nostr_data(1000)

save(notes, "notes")
#notes = load("notes")
