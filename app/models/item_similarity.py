from .models import Item
import gensim
from gensim.matutils import softcossim
from gensim import corpora
import gensim.downloader as api
from gensim.utils import simple_preprocess

class ItemSimilarity():

    class ItemScore():

        def __init__(self, item):
            self.str = item.name + ": " + item.desc
            self.score = 0

        def __lt__(self, other):
            return self.score < other.score

        def __le__(self, other):
            return self.score <= other.score

        def __str__(self):
            return self.str

    def __init__(self, model=None):
        self.itemScores = {}

        if model is None:
            self.model = api.load('fasttext-wiki-news-subwords-300')
        else:
            self.model = model

    def addItem(self, item):
        if isinstance(item, Item):
            self.itemScores[item.Id]

    def addItemCollection(self, items):
        newEntries = {item.Id: ItemScore(item) for item in items}


