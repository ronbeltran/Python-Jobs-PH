
import search
from search.core import porter_stemmer
from posts.models import Entry

for item in Entry.live.all():
    item.save()

search.register(Entry, ('title','body_html', 'meta_description', 'meta_keywords'), indexer=porter_stemmer)
