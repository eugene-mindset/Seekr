from .models import Item
import gensim
from gensim.matutils import softcossim
from gensim import corpora
import gensim.downloader as api
from gensim.utils import simple_preprocess
from gensim.models.keyedvectors import Word2VecKeyedVectors
from gensim.models import WordEmbeddingSimilarityIndex
from gensim.similarities import Similarity, SparseTermSimilarityMatrix, SoftCosineSimilarity

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

    def __init__(self, modelName: str='', filepath: str=''):
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
        self.docsimIndex = None

        # private properties (do not touch, these are important flags)
        self._simOutdated = True
        self._bagOfWordsCalled = False
        self._wordEmbedding = None

        # load the default (fasttext-wiki) model if no modelName is passed,
        # if the name is NoneType, load no model, else load the specified model
        if filepath is not '':
            self.model = Word2VecKeyedVectors.load(filepath)
            self._wordEmbedding = WordEmbeddingSimilarityIndex(self.model)
        elif modelName is None:
            pass
        elif modelName is not '':
            self.model = api.load(modelName)
            self._wordEmbedding = WordEmbeddingSimilarityIndex(self.model)
        else:
            self.model = api.load('fasttext-wiki-news-subwords-300')
            self._wordEmbedding = WordEmbeddingSimilarityIndex(self.model)


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


    def computeBagOfWordsForItems(self):
        """
            Compute the sentences (or the bag of words) for every item listing
            in self.
        """

        for itemScore in self.itemScores:
            itemScore.sentence = self.dictionary.doc2bow(
                simple_preprocess(str(itemScore)))

        self._bagOfWordsCalled = True
        self._simOutdated = True


    def computeSimilarityMatrix(self):
        """
            Compute the similarity matrix of the model
        """

        if self._wordEmbedding is None:
            self._wordEmbedding = WordEmbeddingSimilarityIndex(self.model)

        # create similarity matrix, update flags
        self.simMatrix = SparseTermSimilarityMatrix(self._wordEmbedding, self.dictionary)
        self.docsimIndex = SoftCosineSimilarity([x.sentence for x in self.itemScores], self.simMatrix)
        self._simOutdated = False


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
        if not self._bagOfWordsCalled:
            if computeBag:
                self.computeBagOfWordsForItems()
            else:
                raise TypeError("One ItemScore isntance contains has no "
                                "sentence (bag of words) computed for it yet "
                                "(self.sentence is NoneType)")

        if self._simOutdated:
            if computeSim:
                self.computeSimilarityMatrix()
            else:
                raise TypeError("Similarity matrix for "
                    + repr(self) + " is not up to date with its dictionary, thus"
                    + " cannot the corresponding docsim may not exist.")

        # score every item
        scores = self.docsimIndex[sentence]
        print(scores)
        print(type(scores.tolist()))
        for score, itemScore in zip(self.docsimIndex[sentence].tolist(), self.itemScores):
            itemScore.score = score


    def getSortedItems(self):
        """
            Get the items in self by how well they scored.

            Return
            ------
            list of items sorted by similarity to last compared item
        """

        results = [itemScore for itemScore in self.itemScores]
        results.sort(reverse=True)

        return [itemScore.item for itemScore in results]