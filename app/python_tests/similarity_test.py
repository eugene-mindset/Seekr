import unittest
from app.models import Item
from app.models.similarity import ItemSimilarity

class ItemSimTest(unittest.TestCase):
    def setUp(self):
        """ Using glove-wiki as its a much smaller model, so the test will run a
            lot faster than using the default model"""

        itemSim = ItemSimilarity('glove-wiki-gigaword-50')
        item1 = Item(name="test", desc="")

    def tearDown(self):
        return

    def test_1(self):
        self.assertEqual(1, 1)