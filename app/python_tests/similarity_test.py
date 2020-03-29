import unittest
from app.models import Item
from app.models.similarity import ItemSimilarity
import gensim.downloader as api
from gensim.utils import simple_preprocess

class ItemSimTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Using glove-wiki as its a much smaller model, so the test will run a
            lot faster than using the default model"""
        cls.model = api.load('glove-wiki-gigaword-50')

        cls.item1_1 = Item(name="test", desc="this a test")
        cls.item2_1 = Item(name="apple", desc="a half eaten apple")
        cls.item2_2 = Item(name="apple iphone", desc="model is iphone 7 plus")
        cls.item2_3 = Item(name="phone", desc="lost my iphone")
        cls.item2_4 = Item(name="missing phone", desc="lost my phone somewhere"
                                                    + ", is a google pixel")

    def setUp(self):
        self.itemSim = ItemSimilarity(modelName=None)
        self.itemSim.model = self.model

    def tearDown(self):
        return

    @classmethod
    def tearDownClass(cls):
        return

    def test_add_clear_item(self):
        self.itemSim.addItem(self.item1_1)
        self.assertIs(self.itemSim.itemScores[0].item, self.item1_1)

        prep = simple_preprocess(self.item1_1.name + ': ' + self.item1_1.desc)
        prep = list(set(prep))
        self.assertEqual(len(self.itemSim.dictionary), len(prep))

        self.itemSim.clearItems()
        self.assertEqual(len(self.itemSim.itemScores), 0)

    def test_add_clear_multiple_items(self):
        self.itemSim.addItems([self.item2_1, self.item2_2,
            self.item2_3, self.item2_4])
        self.assertEqual(len(self.itemSim.itemScores), 4)

        self.itemSim.clearItems()
        self.assertEqual(len(self.itemSim.itemScores), 0)

    def test_clear_dict(self):
        self.itemSim.addItem(self.item1_1)
        self.itemSim.clearDictionary()
        self.assertEqual(len(self.itemSim.dictionary), 0)

    def test_compute_dict(self):
        self.itemSim.addItem(self.item1_1)
        self.itemSim.clearDictionary()

        self.itemSim.computeDictionary()
        prep = simple_preprocess(self.item1_1.name + ': ' + self.item1_1.desc)
        prep = list(set(prep))
        self.assertEqual(len(self.itemSim.dictionary), len(prep))

    def test_exception_compute_sim(self):
        with self.assertRaises(Exception) as err:
            self.model = None
            self.itemSim.computeSimilarityMatrix()

    def test_compute_sim_matrx(self):
        self.itemSim.addItem(self.item1_1)
        self.itemSim.computeSimilarityMatrix()

        prep = simple_preprocess(self.item1_1.name + ': ' + self.item1_1.desc)
        prep = list(set(prep))
        self.assertEqual(self.itemSim.simMatrix.shape, (len(prep), len(prep)))
