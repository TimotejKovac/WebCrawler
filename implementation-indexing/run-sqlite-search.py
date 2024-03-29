import os
from processing import format_results, get_snippets, handle_indexing
import sqlite3
import time
import argparse

parser = argparse.ArgumentParser(description='Extracts data from a webpage.')
parser.add_argument('query', metavar='T', type=str, help='query words.')

args = parser.parse_args()

if not os.path.exists("inverted-index.db"):
    handle_indexing()

query = args.query
queries = query.split(" ")

conn = sqlite3.connect('inverted-index.db')
c = conn.cursor()
sub_results = {}
time_before = time.time()

times = 0
for query_word in queries:

    tim_bef = time.time()
    select = "SELECT frequency, documentName, indexes " \
             "FROM Posting WHERE word = ? " \
             "ORDER BY frequency DESC " \
             #"LIMIT 10"

    c.execute(select, (query_word,))
    times += (time.time() - tim_bef)

    for row in c.fetchall():
        frequency, document, indexes = row[0], row[1], row[2]

        if document in sub_results:
            sub_results[document].append((frequency, document, indexes))
        else:
            sub_results[document] = [(frequency, document, indexes)]

print("Results found. Merging results and processing snippets...")
#select1 = "SELECT documentName, frequency FROM Posting ORDER BY frequency DESC LIMIT 10"
#select1 = "SELECT word, documentName, SUM(frequency) AS alt FROM Posting GROUP BY word ORDER BY alt DESC LIMIT 10"


time_taken = (time.time() - time_before) * 1000

results = []
for document, list in sub_results.items():
    results.append((sum(sub[0] for sub in list), document,
                    get_snippets(document, ",".join([sub[2] for sub in list]).split(","))))

results.sort(key=lambda tup: tup[0], reverse=True)  # sorts in place

print(format_results(query, time_taken, results))

print(times)
