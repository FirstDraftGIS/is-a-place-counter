from collections import Counter, defaultdict
from csv import DictReader
from pickle import dump
from re import findall, split
from wake import clean_title, download_if_necessary, get_links, get_valid_english_wikipedia_pages, remove_references
from wake import clean_page_text

def prune_counter(counter):
    pruned = defaultdict(Counter)
    for key, value in list(reversed(sorted(list(counter.items()), key=lambda item: sum(item[1].values()))))[:100000]:
        pruned[key] = value
    return pruned

def run():
    
    try:
        
        url_to_gazetteer = "https://s3.amazonaws.com/firstdraftgis/wikidata-gazetteer.tsv"
        path_to_gazetteer = download_if_necessary(url_to_gazetteer)
        print("path_to_gazetteer:", path_to_gazetteer)    
    
        place_titles = set()
        with open(path_to_gazetteer) as f:
            for line in DictReader(f, delimiter="\t"):
                enwiki_title = line["enwiki_title"]
                if enwiki_title: # probably unnecessary, but playing it safe
                    place_titles.add(enwiki_title)
        print("created place_titles")

        page_count = 0
        
        counter = defaultdict(Counter)

        for page in get_valid_english_wikipedia_pages(debug=False):
            
            #print("valid page:", type(page))
            
            page_count += 1
            
            if page_count % 10000 == 0:
                print("page_count:", page_count)

            page_text = page.find("revision/text").text
            #print("page_text:", type(page_text))
            
            places_in_text = set()

            # this accidentally picks up wikilinks inside of tags
            links = get_links(page_text)

            #print("links:", type(links))
            for link in links:
                if link["title"] in place_titles:
                    places_in_text.add(link["title"])
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

            if len(counter.keys()) > 1500000:
                counter = prune_counter(counter)
                
            #if page_count > 1000:
            #    break

        with open("/tmp/is_a_place_counter.pickle", "wb") as f:
            dump(counter, f)

    except Exception as e:
        print("[is-a-place-counter] found an error", e)
        
        
run()