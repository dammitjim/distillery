import os
import json
from random import randint

from django.core.management.base import BaseCommand
from django.conf import settings

from api.models import Distillery, Country


class Command(BaseCommand):
    STATUS_ACTIVE_PARTIALS = ["active"]

    def handle(self, *args, **kwargs):
        filepath = os.path.join(settings.BASE_DIR, "crawler/whiskybase/output/distilleries.json")
        with open(filepath) as data_file:
            data = json.load(data_file)
            for row in data:
                dist = Distillery(name=row["name"], address=row["address"], url=row["url"], wb_id=row["wb_id"])
                if "founded" in row:
                    dist.founded = row["founded"]
                if "status" in row:
                    dist.active = True if row["status"].lower() in self.STATUS_ACTIVE_PARTIALS else False
                if "website" in row:
                    dist.website = row["website"]
                if "capacity per year" in row:
                    dist.capacity_per_year = row["capacity per year"]
                if "owner" in row:
                    dist.owner = row["owner"]
                if "country" in row:
                    existing_country = Country.objects.filter(name=row["country"]).first()
                    if existing_country:
                        dist.country = existing_country
                    else:
                        new_country = Country.objects.create(name=row["country"]).save()
                        dist.country = new_country
                if "closed" in row:
                    if dist.active:
                        print("active distillery has apparently closed: " + dist.name)
                    dist.closed = row["closed"]

                dist.save()


