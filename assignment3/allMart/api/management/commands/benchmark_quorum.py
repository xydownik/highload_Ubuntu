import time
from django.core.management.base import BaseCommand
from api import models

class Command(BaseCommand):
    help = 'Benchmark read and write operations for KeyValue model'

    def add_arguments(self, parser):
        parser.add_argument('--num-operations', type=int, default=1000,
                            help='Number of operations to benchmark')

    def handle(self, *args, **kwargs):
        num_operations = kwargs['num_operations']
        start_time = time.time()
        for i in range(num_operations):
            models.KeyValue.objects.create(key=f'key_{i}', value=f'value_{i}')  # Writes to the primary database
        write_time = time.time() - start_time
        print(f'Write {num_operations} operations took: {write_time:.2f} seconds')

        # Read Benchmark
        start_time = time.time()
        for i in range(num_operations):
            models.KeyValue.objects.get(key=f'key_{i}')  # Reads the specific keys
        read_time = time.time() - start_time
        print(f'Read {num_operations} operations took: {read_time:.2f} seconds')