from collections import Counter, defaultdict
from csv import DictReader, DictWriter
import pickle
from re import findall, split
from wake import clean_title, download_if_necessary, get_links, get_valid_english_wikipedia_pages, remove_references
from wake import clean_page_text

from config import path_to_place_titles, path_to_pickled_counter, path_to_tsv, path_to_training_data

def prune_counter(counter):
    pruned = defaultdict(Counter)
    for key, value in list(reversed(sorted(list(counter.items()), key=lambda item: sum(item[1].values()))))[:100000]:
        pruned[key] = value
    return pruned

def run():
    
    try:
        
        delimiter = "\t"
        fieldnames=["page_id", "page_title", "yes", "no"]
        with open(path_to_training_data, "w") as f:
            writer = DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()

        # load set of titles for places in wikidata-gazetteer
        # https://github.com/FirstDraftGIS/wikidata-gazetteer#pickled-set
        with open(path_to_place_titles, "rb") as f:
            place_titles = pickle.load(f)

        page_count = 0
        
        counter = defaultdict(Counter)

        for page in get_valid_english_wikipedia_pages(debug=False):
            
            #print("valid page:", type(page))
            
            page_count += 1
            
            if page_count % 10000 == 0:
                print("page_count:", page_count)

            page_id = page['id']
            page_title = page["title"]
            page_text = page["text"]
            #print("page_text:", type(page_text))
            
            places_in_text = set()
            titles_of_places_in_text = set()

            # this accidentally picks up wikilinks inside of tags
            links = get_links(page_text)

            #print("links:", type(links))
            for link in links:
                title = link["title"]
                if title in place_titles:
                    titles_of_places_in_text.add(title)                    
                    places_in_text.add(title)
                    places_in_text.add(link["display_text"])
            
            #print("places_in_text:", len(places_in_text))
            #cleaned_text = clean_page_text(page_text)
            #print("cleaned_text:", cleaned_text)
            
            # need to remove references because can include unlinked locations
            # like location of publisher
            page_text = remove_references(page_text)


            """
                we only want to look at unique tokens
                in order to become more resistant to articles that forget to
                link a place that is mentioned a lot
            """            
            token_counter = Counter(split("[{}\n</>\]\[\(\)-=\|\# ']", page_text))
            #print("tokens:", len(tokens))
            
            tokens_that_are_probably_not_places = set()

            for token, count in token_counter.most_common():
                """
                    Only want tokens that are mentioned more than ten times.
                    Often, places won't be linked if mentioned only a couple times.
                """
                if token and count > 10:
                    if token in places_in_text:
                        counter[token]["yes"] += 1
                    elif all(token not in p for p in places_in_text):
                        counter[token]["no"] += 1
                        if all(char not in token for char in [";","\n",'"',"'","\r","\t"]):  
                            tokens_that_are_probably_not_places.add(token)

            with open(path_to_training_data, "a") as f:
                DictWriter(f, fieldnames=fieldnames, delimiter=delimiter).writerow({
                    "page_id": page_id,
                    "page_title": page_title,
                    "yes": ";".join(titles_of_places_in_text),
                    "no": ";".join(tokens_that_are_probably_not_places)                    
                })

            if len(counter.keys()) > 1500000:
                counter = prune_counter(counter)
                
            #if page_count > 1000:
            #    break

        with open(path_to_pickled_counter, "wb") as f:
            pickle.dump(counter, f)

    except Exception as e:
        print("[is-a-place-counter] found an error", e)
        
        
run()