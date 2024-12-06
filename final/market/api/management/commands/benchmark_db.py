import time
from django.core.management.base import BaseCommand
from django.db import connections

class Command(BaseCommand):
    help = 'Benchmark database read performance'

    def handle(self, *args, **kwargs):
        databases = ['default', 'replica1', 'replica2']
        for db in databases:
            start_time = time.time()
            with connections[db].cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM api_customuser")
                row_count = cursor.fetchone()[0]
            end_time = time.time()
            duration = end_time - start_time
            self.stdout.write(f'{db}: {row_count} rows, {duration:.4f} seconds')
