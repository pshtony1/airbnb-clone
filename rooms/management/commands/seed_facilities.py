from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command creates facilities automatically"

    # def add_arguments(self, parser):
    #     parser.add_argument("--times", help="How many times do you want to tell you?")

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]

        for facitity in facilities:
            room_models.Facility.objects.create(name=facitity)

        self.stdout.write(self.style.SUCCESS(f"✔ {len(facilities)} Facilities Created"))