import os
import json

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        filepath = os.path.join(settings.BASE_DIR, "crawler/whiskybase/output/distilleries.json")
        with open(filepath) as data_file:
            data = json.load(data_file)
            testbed = data[0]
            print(testbed)
