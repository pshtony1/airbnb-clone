from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from rooms import models as room_models
from users import models as user_models
import random


class Command(BaseCommand):

    help = "This command creates reviews automatically"

    def add_arguments(self, parser):
        parser.add_argument("--number", help="How many reviews do you want create?")

    def handle(self, *args, **options):
        number = int(options.get("number"))

        if number < 0:
            self.stdout.write(
                self.style.ERROR("❌ You cannot create negative number of reviews.")
            )
            return

        elif number == 0:
            self.stdout.write(self.style.WARNING("✔ No review created."))
            return

        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        seeder.add_entity(
            review_models.Review,
            number,
            {
                "accuracy": lambda _: random.randint(1, 5),
                "communication": lambda _: random.randint(1, 5),
                "cleanliness": lambda _: random.randint(1, 5),
                "location": lambda _: random.randint(1, 5),
                "check_in": lambda _: random.randint(1, 5),
                "value": lambda _: random.randint(1, 5),
                "room": lambda room: random.choice(all_rooms),
                "user": lambda user: random.choice(all_users),
            },
        )

        seeder.execute()
        self.stdout.write(
            self.style.SUCCESS(
                f"✔ {number} {number == 1 and 'Review' or 'Reviews'} Created!"
            )
        )
