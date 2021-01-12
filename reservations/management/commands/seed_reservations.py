from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations import models as reservation_models
from rooms import models as room_models
from users import models as user_models
import random
from datetime import datetime, timedelta


class Command(BaseCommand):

    help = "This command creates reservations automatically"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", help="How many reservations do you want create?"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))

        if number < 0:
            self.stdout.write(
                self.style.ERROR("❌ You cannot create negative number of reservations.")
            )
            return

        elif number == 0:
            self.stdout.write(self.style.WARNING("✔ No reservation created."))
            return

        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        seeder.add_entity(
            reservation_models.Reservation,
            number,
            {
                "guest": lambda user: random.choice(all_users),
                "room": lambda room: random.choice(all_rooms),
                "check_in": lambda time: datetime.now(),
                "check_out": lambda time: datetime.now()
                + timedelta(days=random.randint(3, 25)),
            },
        )

        seeder.execute()

        self.stdout.write(
            self.style.SUCCESS(
                f"✔ {number} {number == 1 and 'Reservation' or 'Reservations'} Created!"
            )
        )
