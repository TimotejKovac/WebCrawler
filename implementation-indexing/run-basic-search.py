import os
from processing import format_results, get_snippet, handle_indexing, index_pages
import time

if not os.path.exists("inverted-index.db"):
    handle_indexing()

# TODO: Get real query. TK
query = "trgovina"

time_before = time.time()
#TODO: Handle index_pages. TK
index_pages()
time_taken = (time.time() - time_before) * 1000

results = []
for row in c.fetchall():
    frequency, document, indexes = row[0], row[1], row[2]
    snippet = get_snippet(document, indexes.split(","))
    results.append((frequency, document, snippet))

print(format_results(query, time_taken, results))


