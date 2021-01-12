from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models
import random
from copy import deepcopy


class Command(BaseCommand):

    help = "This command creates many rooms automatically"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, help="How many rooms do you want to create?"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))

        if number < 0:
            self.stdout.write(
                self.style.ERROR("❌ You cannot create negative number of rooms.")
            )
            return

        elif number == 0:
            self.stdout.write(self.style.WARNING("✔ No room created."))
            return

        seeder = Seed.seeder()

        all_users = user_models.User.objects.all()
        all_room_types = room_models.RoomType.objects.all()

        if not all_users:
            self.stdout.write(
                self.style.ERROR(
                    "❌ You don't have any user. Please create any user first."
                )
            )
            return

        if not all_room_types:
            self.stdout.write(
                self.style.ERROR(
                    "❌ You don't have any room type. Please create any room type first."
                )
            )
            return

        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda name: seeder.faker.address(),
                "host": lambda user: random.choice(all_users),
                "room_type": lambda rt: random.choice(all_room_types),
                "price": lambda number: random.randint(0, 1000000),
                "guests": lambda number: random.randint(1, 5),
                "beds": lambda number: random.randint(1, 5),
                "bedrooms": lambda number: random.randint(1, 5),
                "baths": lambda number: random.randint(1, 5),
            },
        )

        created_rooms = seeder.execute()
        flatten_pks = flatten(list(created_rooms.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()

        for pk in flatten_pks:
            room = room_models.Room.objects.get(pk=pk)

            for i in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )

            for amenity in amenities:
                r = random.randint(0, 15)

                if r % 2 == 0:
                    room.amenities.add(amenity)

            for facility in facilities:
                r = random.randint(0, 15)

                if r % 2 == 0:
                    room.facilities.add(facility)

            for rule in rules:
                r = random.randint(0, 15)

                if r % 2 == 0:
                    room.house_rules.add(rule)

        self.stdout.write(
            self.style.SUCCESS(
                f"✔ {number} {number == 1 and 'Room' or 'Rooms'} Created!"
            )
        )
