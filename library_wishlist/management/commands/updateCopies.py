from django.core.management.base import BaseCommand, CommandError
from library_wishlist.models import Item, Copy

class Command(BaseCommand):
    args = ''
    help = 'Updates the copies from the catalog of all uncompleted items'

    def handle(self, *args, **options):
        try:
            items = Item.objects.filter(completed=False)

            for i in items:
                i.updateCopies()
                self.stdout.write('Successfully updated item %s' % i)

        except Item.DoesNotExist:
            raise CommandError('There are no items available.')

        self.stdout.write('Successfully updated all items.')
