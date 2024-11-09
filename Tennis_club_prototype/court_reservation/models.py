from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import MyUser
from django_jalali.db.models import jDateField
from datetime import datetime, timedelta

# Base model class for common functionality
class BaseDailyTimeSlot(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="%(class)s_reservations", blank=True, null=True)
    start_time = models.CharField(max_length=5, blank=True, null=True)  # Will be auto-filled in each model
    end_time = models.TimeField(editable=False, blank=True, null=True)  # Calculated based on start_time
    is_available = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        abstract = True
        unique_together = ('reservation', 'start_time')

    def save(self, *args, **kwargs):
        # Calculate end_time as 1 hour after start_time
        if self.start_time:
            start_time_dt = datetime.strptime(self.start_time, '%H:%M')
            self.end_time = (start_time_dt + timedelta(hours=1)).time()
        super().save(*args, **kwargs)

                # Set user to None if is_available is True
        if self.is_available:
            self.user = None

    @property
    def is_reserved(self):
        # Determine if the slot is reserved based on availability and user
        return not self.is_available and self.user is not None

    def __str__(self):
        status = "reserved" if self.is_reserved else "available"
        return f"{self.start_time} - {status}"

# Specific models for each court, inheriting from BaseDailyTimeSlot
class ClayOneReservation(models.Model):
    date = jDateField(unique=True)
    def __str__(self):
        return f"Clay 1 Reservation for {self.date}"

class ClayOneTimeSlot(BaseDailyTimeSlot):
    TIME_CHOICES_30 = [(f"{hour:02d}:30", f"{hour:02d}:30") for hour in range(8, 21)]
    reservation = models.ForeignKey(ClayOneReservation, on_delete=models.CASCADE, related_name="time_slots")
    start_time = models.CharField(max_length=5, choices=TIME_CHOICES_30)

class ClayTwoReservation(models.Model):
    date = jDateField(unique=True)
    def __str__(self):
        return f"Clay 2 Reservation for {self.date}"

class ClayTwoTimeSlot(BaseDailyTimeSlot):
    TIME_CHOICES_30 = [(f"{hour:02d}:30", f"{hour:02d}:30") for hour in range(8, 21)]
    reservation = models.ForeignKey(ClayTwoReservation, on_delete=models.CASCADE, related_name="time_slots")
    start_time = models.CharField(max_length=5, choices=TIME_CHOICES_30)

class ClayThreeReservation(models.Model):
    date = jDateField(unique=True)
    def __str__(self):
        return f"Clay 3 Reservation for {self.date}"

class ClayThreeTimeSlot(BaseDailyTimeSlot):
    TIME_CHOICES_00 = [(f"{hour:02d}:00", f"{hour:02d}:00") for hour in range(8, 21)]
    reservation = models.ForeignKey(ClayThreeReservation, on_delete=models.CASCADE, related_name="time_slots")
    start_time = models.CharField(max_length=5, choices=TIME_CHOICES_00)

class ClayFourReservation(models.Model):
    date = jDateField(unique=True)
    def __str__(self):
        return f"Clay 4 Reservation for {self.date}"

class ClayFourTimeSlot(BaseDailyTimeSlot):
    TIME_CHOICES_00 = [(f"{hour:02d}:00", f"{hour:02d}:00") for hour in range(8, 21)]
    reservation = models.ForeignKey(ClayFourReservation, on_delete=models.CASCADE, related_name="time_slots")
    start_time = models.CharField(max_length=5, choices=TIME_CHOICES_00)



# Signals to auto-fill time slots for each reservation model
def create_time_slots(reservation, TimeSlotModel, time_choices):
    """Utility function to create time slots for a reservation"""
    for time in time_choices:
        TimeSlotModel.objects.get_or_create(reservation=reservation, start_time=time[0])

@receiver(post_save, sender=ClayOneReservation)
def create_clayone_time_slots(sender, instance, created, **kwargs):
    if created:
        create_time_slots(instance, ClayOneTimeSlot, ClayOneTimeSlot.TIME_CHOICES_30)

@receiver(post_save, sender=ClayTwoReservation)
def create_claytwo_time_slots(sender, instance, created, **kwargs):
    if created:
        create_time_slots(instance, ClayTwoTimeSlot, ClayTwoTimeSlot.TIME_CHOICES_30)

@receiver(post_save, sender=ClayThreeReservation)
def create_claythree_time_slots(sender, instance, created, **kwargs):
    if created:
        create_time_slots(instance, ClayThreeTimeSlot, ClayThreeTimeSlot.TIME_CHOICES_00)

@receiver(post_save, sender=ClayFourReservation)
def create_clayfour_time_slots(sender, instance, created, **kwargs):
    if created:
        create_time_slots(instance, ClayFourTimeSlot, ClayFourTimeSlot.TIME_CHOICES_00)
