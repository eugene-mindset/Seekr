from .models import Item
import gensim
from gensim.matutils import softcossim
from gensim import corpora
import gensim.downloader as api
from gensim.utils import simple_preprocess

import sys

class ItemSimilarity():
    """
        Class to handle calculating the similarity of item listings based on
        their name and description using soft cosine similarity.
    """

    class ItemScore():
        """
            Is a wrapper class for item listings passed into the class, as well
            as having additional properties to help compute necessary
            information.
        """

        def __init__(self, item):
            self.item = item
            self.sentence = None
            self.score = 0

        def __lt__(self, other):
            return self.score < other.score

        def __le__(self, other):
            return self.score <= other.score

        def __str__(self):
            return self.item.name.lower() + ": " + self.item.desc.lower()

    def __init__(self, modelName: str=''):
        """
            Creates the class.

            Parameters
            ----------

            modelName:str
                name of the model to download through gensim
        """

        # public properties
        self.itemScores = []
        self.dictionary = corpora.Dictionary()
        self.model = None
        self.simMatrix = None

        # private properties (do not touch, these are important flags)
        self._simOutdated = True
        self._bagOfWordsCalled = False

        # load the default (fasttext-wiki) model if no modelName is passed,
        # if the name is NoneType, load no model, else load the specified model
        if modelName is '':
            self.model = api.load('fasttext-wiki-news-subwords-300')
        elif modelName is None:
            pass
        else:
            self.model = api.load(modelName)

    def addItem(self, item):
        """
            Add `item` to use for computing its similarity to queried items.

            Parameters
            ----------

            item: Item
                item to add to 'self'
        """

        # create new ItemScore and dictionary entries from ItemScore
        newEntry = self.ItemScore(item)
        newDictEntry = corpora.Dictionary([simple_preprocess(str(newEntry))])

        # add new entries to items and dictionary, update flags
        self.itemScores.append(newEntry)
        self.dictionary.merge_with(newDictEntry)
        self._simOutdated = True
        self._bagOfWordsCalled = False

    def addItems(self, items):
        """
            Add every item in `items` to use for computing its similarity
            to queried items.

            Parameters
            ----------

            items: list of Item
                items to add to 'self'
        """

        # create new ItemScores and dictionary entries from ItemScore
        newEntries = [self.ItemScore(item) for item in items]
        newDictEntries = corpora.Dictionary(
            [simple_preprocess(str(newScore)) for newScore in newEntries])

        # add new entries to items and dictionary, update flags
        self.itemScores = self.itemScores + newEntries
        self.dictionary.merge_with(newDictEntries)
        self._simOutdated = True
        self._bagOfWordsCalled = False

    def clearItems(self):
        """
            Get rid of item scores in the class
        """

        self.itemScores = []

    def clearDictionary(self):
        """
            Git rid of dictionary entries from previous item listings
        """

        self.dictionary = corpora.Dictionary()
        self._bagOfWordsCalled = False

    def computeDictionary(self):
        """
            Compute the dictionary from all the item listings in the class.
        """

        self.dictionary = corpora.Dictionary(
            [simple_preprocess(str(item)) for item in self.itemScores])
        self._bagOfWordsCalled = False

    def computeSimilarityMatrix(self):
        """
            Compute the similarity matrix of the model
        """

        # raise exception if model is not defined
        if self.model is None:
            raise TypeError("self.model is NoneType, cannot make "
                "similarity matrix with NoneType")

        # create similarity matrix, update flags
        self.simMatrix = self.model.similarity_matrix(dictionary, tfidf=None,
            threshold=0.0, exponent=2.0, nonzero_limit=100)
        self._simOutdated = False

    def computeBagOfWordsForItems(self):
        """
            Compute the sentences (or the bag of words) for every item listing
            in self.
        """

        for itemScore in self.itemScores:
            itemScore.sentence = self.dictionary.doc2bow(
                simple_preprocess(str(itemScore)))

        self._bagOfWordsCalled = True

    def _computeSimilarity(self, sent1, sent2):
        """
            Compute soft cosine similarity between `sent1` and `sent2`.

            Parameters
            ----------
            sent1:
                query sentence

            sent2:
                compared sentence

            Return
            ------
            float from -1 to 1 of how similar the two sentences are,
            the higher the better
        """

        return softcossim(sent1, sent2, self.simMatrix)

    def scoreItems(self, itemToCompare, computeSim=False, computeBag=False):
        """
            Score every item listing in self. The score is how similar that item
            is to `itemToCompare`.

            Parameters
            ----------
            itemToCompare: Item
                item to see how similar it is to other items

            computeSim=False: bool
                If true, will automatically update simMatrix

            computeBag=False: bool
                If true, will automatically update every items sentence
                (bag of words)
        """


        # make itemToCompare's bag of words
        sentence = self.dictionary.doc2bow(
            simple_preprocess(str(self.ItemScore(itemToCompare))))

        # based on flags and parameters, update information or
        # send errors/warnings
        if self._simOutdated:
            if computeSim:
                self.computeSimilarityMatrix()
            else:
                sys.stderr.write("Warning: similarity matrix for "
                    + repr(self) + " is not up to date with its dictionary.\n")

        if not self._bagOfWordsCalled:
            if computeBag:
                self.computeBagOfWordsForItems()
            else:
                raise TypeError("One ItemScore isntance contains has no "
                                "sentence (bag of words) computed for it yet "
                                "(self.sentence is NoneType)")

        # score every item
        for item in self.itemScores:
            item.score = self._computeSimilarity(sentence, item.sentence)

    def getSortedItems(self):
        """
            Get the items in self by how well they scored.

            Return
            ------
            list of items sorted by similarity to last compared item
        """

        results = [itemScore for itemScore in self.itemScores]
        results.sort()

        return [itemScore.item for item in results]