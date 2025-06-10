from django.core.management.base import BaseCommand
from django.core import management
import os

class Command(BaseCommand):
    help = "Load data from fixtures/data.json"

    def handle(self, *args, **options):
        fixture_path = 'fixtures/data.json'
        if not os.path.exists(fixture_path):
            self.stderr.write(f"Fixture file {fixture_path} not found!")
            return

        self.stdout.write(f"Loading data from {fixture_path} ...")
        management.call_command('loaddata', fixture_path)
        self.stdout.write(self.style.SUCCESS("Data loaded successfully."))
