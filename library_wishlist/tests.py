from django.test import TestCase
from django.utils.timezone import now
from parser import search_catalog
from models import Item, Copy, Branch

class ItemTestCase(TestCase):
    def setUp(self):
        Item.objects.create(text="Bombay Bicycle Club")

    def test_item_has_text(self):
        test_item = Item.objects.get(text="Bombay Bicycle Club")
        self.assertEqual(test_item.text, "Bombay Bicycle Club")

    def test_item_search_catalog_with_invalid_text(self):
        text="Bombays Bicycle Clubb" # with typos
        search_item = search_catalog(text)

        self.assertEqual(search_item, [])

    # saving the searchitem to reduce latency
    search_item = None

    def test_item_search_catalog_with_valid_item_text(self):
        """Search the catalog for this item text"""
        test_item = Item.objects.get(text="Bombay Bicycle Club")
        search_item = search_catalog(test_item.text)

        self.assertEqual(search_item['name'], 'So long, see you tomorrow')

    def test_item_has_valid_date(self):
        pass


    '''
        # Test Todos:
        - delete item, branch, copy
        - test valid item date
        - test create copies (single and list)
        - test Copy model with item
        - test item lists
        - test valid searchIndex with new catalog search
        - test management command with update copies
        - test views...
    '''
