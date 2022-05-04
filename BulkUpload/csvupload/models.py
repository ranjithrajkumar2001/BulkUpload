import csv
import os.path

from django.db import models
import uuid
import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver


class Patient(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    patient_id = models.CharField(max_length=256, default=None, blank=False)
    first_name = models.CharField(max_length=256, default=None, blank=False)
    last_name = models.CharField(max_length=256, default=None, blank=False)
    email_address = models.EmailField(unique=True, default=None, blank=False)
    date_of_birth = models.DateField(blank=False)
    eligible_for_insurance = models.CharField(max_length=3, default=None, blank=False)
    created_datetime = models.DateTimeField(default=None, blank=False)

