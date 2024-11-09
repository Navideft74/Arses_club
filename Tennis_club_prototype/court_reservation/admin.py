from django.contrib import admin
from .models import (
    ClayOneReservation, 
    ClayOneTimeSlot, 
    ClayTwoReservation, 
    ClayTwoTimeSlot, 
    ClayThreeReservation, 
    ClayThreeTimeSlot, 
    ClayFourReservation, 
    ClayFourTimeSlot 
)
from accounts.models import MyUser

# Abstract inline admin class for time slots
class TimeSlotMain(admin.TabularInline):
    fields = ('start_time', 'user', 'is_available', 'is_paid')
    readonly_fields = ('start_time',)
    autocomplete_fields = ['user']
    extra = 0  # No extra empty slots
    can_delete = False
    
    class Meta:
        abstract = True

# Inline admin classes for each court time slot model
class DailyTimeSlotClayOneInline(TimeSlotMain):
    model = ClayOneTimeSlot

class DailyTimeSlotClayTwoInline(TimeSlotMain):
    model = ClayTwoTimeSlot

class DailyTimeSlotClayThreeInline(TimeSlotMain):
    model = ClayThreeTimeSlot

class DailyTimeSlotClayFourInline(TimeSlotMain):
    model = ClayFourTimeSlot

# Base reservation admin with custom inline handling and redirect
class BaseReservationAdmin(admin.ModelAdmin):
    list_display = ('date',)
    list_filter = ('date',)

    def get_inlines(self, request, obj=None):
        # Show inlines only if the reservation instance exists
        if obj is not None:
            return self.inlines
        return []

    def response_add(self, request, obj, post_url_continue=None):
        # Redirect to the change view after adding a new reservation
        return super().response_add(request, obj, post_url_continue or f'../{obj.pk}/change/')

# Admin classes for each court reservation model
@admin.register(ClayOneReservation)
class ClayOneReservationAdmin(BaseReservationAdmin):
    inlines = [DailyTimeSlotClayOneInline]

@admin.register(ClayTwoReservation)
class ClayTwoReservationAdmin(BaseReservationAdmin):
    inlines = [DailyTimeSlotClayTwoInline]

@admin.register(ClayThreeReservation)
class ClayThreeReservationAdmin(BaseReservationAdmin):
    inlines = [DailyTimeSlotClayThreeInline]

@admin.register(ClayFourReservation)
class ClayFourReservationAdmin(BaseReservationAdmin):
    inlines = [DailyTimeSlotClayFourInline]
