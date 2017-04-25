import json
import os

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        if len(options["path"]) == 0:
            raise CommandError("no path supplied")
        path = os.path.abspath(options["path"][0])
        cols = {}
        with open(path) as raw_data:
            data = json.load(raw_data)
            for row in data:
                for key in row:
                    if key not in cols:
                        cols[key] = 1
                    else:
                        cols[key] += 1
        print(cols)
