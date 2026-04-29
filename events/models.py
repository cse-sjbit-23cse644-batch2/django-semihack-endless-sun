from django.db import models
import uuid


# =======================
# EVENT MODEL
# =======================
class Event(models.Model):
    EVENT_TYPES = [
        ('FEST', 'Fest Event'),
        ('DRIVE', 'Placement Drive'),
    ]

    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.get_event_type_display()})"


# =======================
# STAGE MODEL
# =======================
class Stage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=100)   # Aptitude, GD, Interview
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.event.name} — {self.name}"


# =======================
# PARTICIPANT MODEL
# =======================
class Participant(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')

    transaction_id = models.CharField(max_length=100, unique=True)
    receipt = models.FileField(upload_to='receipts/')

    # ✅ IMPORTANT FIELDS
    transaction_verified = models.BooleanField(default=False)
    feedback_submitted = models.BooleanField(default=False)

    certificate_hash = models.CharField(max_length=100, unique=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-generate certificate hash
        if not self.certificate_hash:
            self.certificate_hash = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.student_id})"


# =======================
# ATTENDANCE MODEL
# =======================
class Attendance(models.Model):
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    stage = models.ForeignKey(
        Stage,
        on_delete=models.CASCADE,
        related_name='attendances'
    )

    # ✅ IMPORTANT FIELD (use this everywhere)
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('participant', 'stage')

    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.participant.name} — {self.stage.name} — {status}"


# =======================
# FEEDBACK MODEL
# =======================
class Feedback(models.Model):
    participant = models.OneToOneField(
        Participant,
        on_delete=models.CASCADE,
        related_name='feedback'
    )

    rating = models.IntegerField()
    comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.participant.name} — {self.rating}/5"