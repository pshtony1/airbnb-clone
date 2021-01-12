from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from rooms import models as room_models
from users import models as user_models
import random


class Command(BaseCommand):

    help = "This command creates lists automatically"

    def add_arguments(self, parser):
        parser.add_argument("--number", help="How many lists do you want create?")

    def handle(self, *args, **options):
        number = int(options.get("number"))

        if number < 0:
            self.stdout.write(
                self.style.ERROR("❌ You cannot create negative number of lists.")
            )
            return

        elif number == 0:
            self.stdout.write(self.style.WARNING("✔ No list created."))
            return

        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        seeder.add_entity(
            list_models.List,
            number,
            {
                "user": lambda user: random.choice(all_users),
            },
        )

        created_lists = seeder.execute()
        flattened_pks = flatten(list(created_lists.values()))

        for pk in flattened_pks:
            _list = list_models.List.objects.get(pk=pk)
            to_add = all_rooms[
                random.randint(0, len(all_rooms) // 2) : random.randint(
                    len(all_rooms) // 2 + 1, len(all_rooms)
                )
            ]
            _list.rooms.add(*to_add)

        self.stdout.write(
            self.style.SUCCESS(
                f"✔ {number} {number == 1 and 'List' or 'Lists'} Created!"
            )
        )
