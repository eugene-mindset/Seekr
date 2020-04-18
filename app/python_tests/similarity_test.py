import unittest

import gensim.downloader as api

from app.models import Item
from app.models.similarity import ItemSimilarity


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
        self.itemSim = ItemSimilarity(self.model)

    def tearDown(self):
        return

    @classmethod
    def tearDownClass(cls):
        return

    def test_add_clear_item(self):
        self.itemSim.addItem(self.item1_1)
        self.assertIs(self.itemSim.itemScores[0].item, self.item1_1)

        prep = self.itemSim.preprocess(self.item1_1.name + ': ' + self.item1_1.desc)
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
        prep = self.itemSim.preprocess(self.item1_1.name + ': ' + self.item1_1.desc)
        prep = list(set(prep))
        self.assertEqual(len(self.itemSim.dictionary), len(prep))

    def test_score_items(self):
        self.itemSim.addItem(self.item1_1)
        self.itemSim.addItem(self.item2_1)

        self.itemSim.scoreItems(self.item1_1)
        results = self.itemSim.getSortedItems()
        self.assertEqual(results, [self.item1_1, self.item2_1])
