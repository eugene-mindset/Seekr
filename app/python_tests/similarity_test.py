import unittest
from app.models import Item
from app.models.item_similarity import ItemSimilarity

class ItemSimTest(unittest.TestCase):
    def setUp(self):
        itemSim = ItemSimilarity([])

    def tearDown(self):
        return

    def test_1(self):
        self.assertEqual(1, 1)