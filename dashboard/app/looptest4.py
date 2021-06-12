animals = [
    {'name':'cow', 'size':'large'},
    {'name':'bird', 'size':'small'},
    {'name':'fish', 'size':'small'},
    {'name':'rabbit', 'size':'medium'},
    {'name':'pony', 'size':'large'},
    {'name':'squirrel', 'size':'medium'},
    {'name':'fox', 'size':'medium'}]
import itertools
from operator import itemgetter
sorted_animals = sorted(animals, key=itemgetter('size'))
for key, group in itertools.groupby(sorted_animals, key=lambda x:x['size']):
    print (key),
    print (list(group))