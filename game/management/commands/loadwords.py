from django.core.management.base import BaseCommand
from game.models import Word

WORDS = [
    'APPLE','MANGO','GRAPE','WATER','HOUSE',
    'PLANT','BERRY','PEACH','LEMON','BREAD',
    'CHAIR','TABLE','PHONE','LIGHT','PAPER',
    'SHARP','GLASS','PAINT','TRAIN','MOUSE'
]

class Command(BaseCommand):
    help = 'Load 20 initial words'

    def handle(self, *args, **options):
        for w in WORDS:
            Word.objects.get_or_create(word=w)
        self.stdout.write(self.style.SUCCESS('Loaded 20 words!'))
