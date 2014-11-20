from django.test import TestCase
from django.utils.timezone import now
from parser import search_catalog
from models import Item, Copy, Branch
from django.db.models.base import ObjectDoesNotExist

class ItemTestCase(TestCase):
    testItemSingle = None
    testItemMultiple = None
    testBranch = None
    search_item = None

    def setUp(self):
        self.testItemSingle = Item.objects.create(text="Bombay Bicycle Club")
        self.testItemMultiple = Item.objects.create(text="Coldplay")
        self.testBranch = Branch.objects.create(name="Kirschgarten")

        # saving the searchitem to reduce latency
        self.search_item = search_catalog(self.testItemSingle.text)
        self.testItemSingle.createCopies(self.search_item)

        # define fixtures states
        # - amount of copies
        # - copies statuses

    def test_item_has_text(self):
        self.assertEqual(self.testItemSingle.text, "Bombay Bicycle Club")

    def test_item_search_catalog_with_valid_item_text(self):
        """Search the catalog for this item text"""
        self.testItemSingle = Item.objects.get(text="Bombay Bicycle Club")

        self.assertEqual(self.search_item['name'], 'So long, see you tomorrow')

    def test_item_search_catalog_with_invalid_text(self):
        text="Bombays Bicycle Clubb" # with typos
        self.search_item = search_catalog(text)

        self.assertEqual(self.search_item, [])

    def test_item_has_valid_date(self):
        """Create new item and test if it's date is equal to now"""
        right_now = now()
        self.testItemSingle.created = right_now

        self.assertEqual(self.testItemSingle.created, right_now)

    def test_delete_item(self):
        testItemSingle = Item.objects.create(text="Bombay Bicycle Club")
        testItemSingle.delete()
        try:
            Item.objects.get(id=testItemSingle.id)
        except ObjectDoesNotExist, e:
            self.assertRaises(e)

    def test_complete_item(self):
        self.assertEqual(self.testItemSingle.completed, False)
        self.testItemSingle.completed = True
        self.assertEqual(self.testItemSingle.completed, True)

    def test_item_create_copies(self):
        self.assertEqual(self.testItemSingle.copies.count(), 1)
        self.assertEqual(self.testItemSingle.copies.all()[0].item.id, self.testItemSingle.id)

    def test_item_set_item_status(self):
        self.testItemSingle.setItemStatus()
        # should be True if Item is available
        self.assertEqual(self.testItemSingle.status, True)

    def test_copies_with_item(self):
        test_copies = Copy.objects.filter(item=self.testItemSingle)
        self.assertEqual(test_copies.count(), self.testItemSingle.copies.count())

    def test_item_with_multiple_search_results(self):
        pass

    def test_item_search_index(self):
        pass


    '''
        # Test Todos:
        - delete item, branch, copy
        - test valid item date
        - test create copies (single and list)
        - test Copy model with item
        - test item lists
        - test valid searchIndex with new catalog search
        - test views...
        - test User
    '''
