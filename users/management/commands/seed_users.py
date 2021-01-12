from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates many users automatically"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="How many users do you want to create?"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))

        if number < 0:
            self.stdout.write(
                self.style.ERROR("❌ You cannot create negative number of users.")
            )
            return

        elif number == 0:
            self.stdout.write(self.style.WARNING("✔ No user created."))
            return

        seeder = Seed.seeder()

        seeder.add_entity(
            user_models.User,
            number,
            {
                "is_staff": False,
                "is_superuser": False,
            },
        )

        seeder.execute()
        self.stdout.write(
            self.style.SUCCESS(
                f"✔ {number} {number == 1 and 'User' or 'Users'} Created!"
            )
        )
