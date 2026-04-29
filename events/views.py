from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, FileResponse
from django.views.decorators.http import require_POST
from .forms import RegistrationForm, FeedbackForm
from .models import Participant, Attendance, Stage, Event, Feedback
from .utils import is_eligible, generate_pdf
import qrcode
import uuid
import os
from django.conf import settings
from io import BytesIO
from django.core.files.base import ContentFile


def home(request):
    return render(request, 'home.html')


# ─── Track A ───────────────────────────────────────────────

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save(commit=False)

            # certificate_hash is auto-set in model's save()
            # but we need it now to generate QR — so set it manually here
            participant.certificate_hash = uuid.uuid4().hex
            participant.save()

            # Generate QR code pointing to verify URL
            verify_url = request.build_absolute_uri(
                f'/verify/{participant.certificate_hash}/'
            )
            qr = qrcode.make(verify_url)
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            filename = f'qr_{participant.student_id}.png'
            participant.qr_code.save(filename, ContentFile(buffer.getvalue()), save=True)

            return redirect('confirm', hash=participant.certificate_hash)
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def confirm(request, hash):
    participant = get_object_or_404(Participant, certificate_hash=hash)
    return render(request, 'confirm.html', {'participant': participant})


# ─── Track B ───────────────────────────────────────────────

def admin_dashboard(request):
    events = Event.objects.prefetch_related('stages', 'participants').all()

    dashboard_data = []
    for event in events:
        stages = list(event.stages.all())
        participants = list(event.participants.all())

        # Build attendance matrix: {participant_id: {stage_id: present}}
        matrix = {}
        for p in participants:
            matrix[p.id] = {}
            for s in stages:
                matrix[p.id][s.id] = False  # default absent

        # Fill in actual attendance records
        attendances = Attendance.objects.filter(
            participant__event=event
        ).select_related('participant', 'stage')

        for att in attendances:
            if att.participant_id in matrix:
                matrix[att.participant_id][att.stage_id] = att.present

        dashboard_data.append({
            'event': event,
            'stages': stages,
            'participants': participants,
            'matrix': matrix,
        })

    return render(request, 'admin_dashboard.html', {'dashboard_data': dashboard_data})


@require_POST
def toggle_attendance(request, participant_id, stage_id):
    attendance, created = Attendance.objects.get_or_create(
        participant_id=participant_id,
        stage_id=stage_id
    )
    attendance.present = not attendance.present
    attendance.save()
    return JsonResponse({'present': attendance.present})


# ─── Track C ───────────────────────────────────────────────

def submit_feedback(request, participant_id):
    participant = get_object_or_404(Participant, id=participant_id)

    if participant.feedback_submitted:
        return render(request, 'feedback.html', {
            'participant': participant,
            'already_submitted': True,
        })

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            Feedback.objects.update_or_create(
                participant=participant,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comments': form.cleaned_data['comments'],
                }
            )
            participant.feedback_submitted = True
            participant.save()
            return redirect('confirm', hash=participant.certificate_hash)
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {
        'participant': participant,
        'form': form,
        'already_submitted': False,
    })

import qrcode
from django.core.files.base import ContentFile
from io import BytesIO

def generate_qr(participant, request):
    qr_data = request.build_absolute_uri(
        f"/verify/{participant.certificate_hash}/"
    )

    qr = qrcode.make(qr_data)

    buffer = BytesIO()
    qr.save(buffer, format='PNG')

    file_name = f"qr_{participant.certificate_hash}.png"

    participant.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=True)
def download_certificate(request, certificate_hash):
    participant = get_object_or_404(Participant, certificate_hash=certificate_hash)

    if not is_eligible(participant):
        return HttpResponseForbidden(
            "Not eligible yet. Requirements: transaction verified + attended at least one stage + feedback submitted."
        )

    buffer = generate_pdf(participant)
    filename = f"certificate_{participant.student_id}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)


def verify_certificate(request, certificate_hash):
    try:
        participant = Participant.objects.get(certificate_hash=certificate_hash)
        return render(request, 'verify.html', {'participant': participant, 'valid': True})
    except Participant.DoesNotExist:
        return render(request, 'verify.html', {'valid': False})


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Event, Participant, Stage

from django.shortcuts import redirect
from .models import Participant

def verify_payment(request, pid):
    p = Participant.objects.get(id=pid)
    p.transaction_verified = True   # ✅ MUST match template
    p.save()
    return redirect('/dashboard/')

