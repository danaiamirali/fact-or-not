"""
A search tool wrapper that can be used to search for information on the internet.

Requires: 
    - A query to be passed in as an argument.

Usage:
    search = Searcher()
    search.search('When did world was 2 end')
    # Output: "{'url': 'https://www.thoughtco.com/when-did-world-war-2-end-3878473', 
    'content': "When and How Did World War II End?\nThere are three dates for the 
    conflict's end, with a separate date for Russia\nBettmann/Contributor/Getty 
    Images\nWorld War II ended with the unconditional surrender of Germany in May 
    1945, but both May 8 and May 9 are celebrated as Victory in Europe Day 
    (or V-E Day)..."

"""

class Searcher():
    name = "Internet Searcher"
    description = "A tool that can be used to search for information on the internet."
    def __init__(self):
        # TO DO
        pass

    def search(self, query: str) -> dict:
        # TO DO
        pass