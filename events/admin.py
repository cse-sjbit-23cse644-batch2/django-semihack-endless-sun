from django.contrib import admin
from .models import Event, Stage, Participant, Attendance, Feedback


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_type', 'date']
    list_filter = ['event_type']


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'order']
    list_filter = ['event']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_id', 'event', 'transaction_id', 'transaction_verified', 'feedback_submitted']
    list_filter = ['event', 'transaction_verified', 'feedback_submitted']
    search_fields = ['name', 'student_id', 'transaction_id']
    # Admin can toggle transaction_verified directly from list view
    list_editable = ['transaction_verified']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['participant', 'stage', 'present']
    list_filter = ['stage', 'present']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['participant', 'rating', 'submitted_at']