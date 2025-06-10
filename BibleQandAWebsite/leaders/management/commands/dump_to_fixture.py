from django.core.management.base import BaseCommand
from django.core import management

class Command(BaseCommand):
    help = "Dump data to fixtures/data.json"

    def handle(self, *args, **options):
        self.stdout.write("Dumping data to fixtures/data.json ...")
        management.call_command(
            'dumpdata',
            exclude=['auth.permission', 'contenttypes'],
            output='fixtures/data.json',
            indent=2,
        )
        self.stdout.write(self.style.SUCCESS("Data dumped successfully."))
