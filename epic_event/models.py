from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    pass


class Client(models.Model):

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="sales_contact_client",
        null=True,
        default="",
    )


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="sales_contact_contract",
        null=True,
    )
    client = models.ForeignKey(
        "Client", on_delete=models.PROTECT, related_name="contracts"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()


class Event(models.Model):
    choices = [
        (1, "created"),
        (2, "assigned"),
        (3, "in progress"),
        (4, "ready"),
        (5, "finished"),
    ]
    contract = models.OneToOneField(
        "Contract", on_delete=models.PROTECT, related_name="event"
    )
    support_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="support_contact_event",
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    event_status = models.IntegerField(choices=choices, default=1)
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField(max_length=1000, null=True)
