from django.db import models
from django.utils import timezone
from django.utils.dateparse import parse_date
from core import models as core_models


def get_now_date():
    now = timezone.now().date()
    now = parse_date(timezone.localtime().strftime("%Y-%m-%d"))

    return now


class Reservation(core_models.TimeStampedModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        choices=STATUS_CHOICES, max_length=12, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reservations"
    )
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="reservations"
    )

    def __str__(self):
        return f"{self.room} / {self.guest} - {self.check_in} ~ {self.check_out}"

    def in_progress(self):
        now = get_now_date()
        return now > self.check_in and now < self.check_out

    def is_finished(self):
        now = get_now_date()
        return now > self.check_out

    in_progress.boolean = True
    is_finished.boolean = True