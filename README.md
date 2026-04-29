# CampusVault
End-to-end event and placement drive management for college campuses.

---

## Project Details

| Field | Details |
|---|---|
| **Theme** | Event Lifecycle and Certification |
| **Team Members** | @Anika Varsha Shekar, @Apoorva S, @D Poojitha, @G Samyak |
| **Live URL** | https://campusvault-app.onrender.com |

---

## Overview

CampusVault is a full-stack web application that digitises the end-to-end lifecycle of college events and placement drives — from student registration to verified certificate generation. Built for institutions that still rely on paper forms, manual attendance sheets, and emailed certificates, CampusVault consolidates everything into a single Django-powered platform. Admins manage events, verify payments, and track attendance; students register, submit feedback, and download tamper-proof PDFs — all without a single sheet of paper changing hands.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django (MVT architecture) |
| **Database** | SQLite (dev / hackathon), PostgreSQL-compatible |
| **Frontend** | HTML5, CSS3, Vanilla JS (AJAX via `fetch()`) |
| **PDF Generation** | ReportLab |
| **Image / QR** | Pillow |
| **Deployment** | Render (with Gunicorn) |

---

## Features

- **Event & Stage Management** — Admins create events with multiple stages (rounds/sessions) via the Django admin panel
- **Student Registration** — Registration form with receipt upload, extension/size validation, and duplicate-entry checks
- **QR Code Generation** — Unique QR code issued per participant on successful registration, used for identity verification
- **Payment Verification** — Admin marks transactions as verified before a student can proceed through the workflow
- **AJAX Attendance Dashboard** — Toggle per-student attendance per stage in real time without page reloads
- **Eligibility Gating** — Certificate unlocks only when payment is verified, all stages attended, and feedback submitted
- **PDF Certificate Generation** — ReportLab generates a Participation Certificate (FEST) or Interview Experience Letter (DRIVE) based on event type
- **QR-based Certificate Verification** — Anyone can verify a certificate's authenticity at `/verify/<hash>/` — no login required
- **SDG-aligned Design** — Supports SDG 4 (Quality Education) and SDG 8 (Decent Work) through digitised, accountable academic record-keeping

---

## CO-SDG Mapping

| Course Outcome | How This Project Demonstrates It | SDG Target Addressed |
|---|---|---|
| CO1: MVT Architecture | CampusVault is built on Django's Model-View-Template pattern — models define Event/Participant/Attendance, views handle all logic, templates render the UI | SDG 4.5 |
| CO2: Models & Forms | Five relational models (Event, Stage, Participant, Attendance, Feedback) with validated ModelForms including file type, size, and duplicate checks | SDG 9.5 |
| CO3: AJAX & Dynamic UI | Attendance dashboard uses fetch() POST with CSRF token to toggle presence per student per stage without page reload | SDG 9.b |
| CO4: File Handling | Receipt upload with extension and size validation; QR code generation using Pillow saved to media/qrcodes/ | SDG 4.4 |
| CO5: PDF Generation | ReportLab generates Participation Certificate (FEST) or Interview Experience Letter (DRIVE) gated behind eligibility logic | SDG 8.6 |

---

## SDG Justification

CampusVault directly advances **SDG 4 (Quality Education)** and **SDG 8 (Decent Work and Economic Growth)** by digitising the entire lifecycle of college events and placement drives. By automating registration, attendance tracking, and certificate generation, the system reduces administrative overhead and eliminates paper-based processes, making institutional record-keeping more reliable and accessible. The eligibility gating — requiring verified payment, confirmed attendance, and submitted feedback before a certificate is issued — ensures academic integrity and accountability. The QR-based certificate verification system allows employers and institutions to instantly validate participation, directly supporting SDG 8.6 by improving the credibility of student credentials. The placement drive module specifically aids students in documenting interview experience, building a verifiable portfolio of engagement. By providing a free, open-source Django template for this workflow, CampusVault enables colleges with limited resources to implement professional-grade event infrastructure, supporting SDG 4.5's goal of equal access to quality education.

---

## Setup Instructions

```bash
git clone [https://github.com/cse-sjbit-23cse644-batch2/django-semihack-endless-sun.git]
cd campusvault_project

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open:
- `http://127.0.0.1:8000` — main app
- `http://127.0.0.1:8000/admin/` — admin panel (create Events and Stages here first)

---

## Full User Flow

```
/register/                     →  Student fills form, uploads receipt
/confirm/<hash>/               →  QR code displayed on screen
/admin/                        →  Admin sets transaction_verified = True
/dashboard/                    →  Admin toggles attendance per stage (AJAX, no refresh)
/feedback/<participant_id>/    →  Student submits rating + comments
/certificate/<hash>/           →  PDF downloads (only if all conditions met)
/verify/<hash>/                →  Anyone can verify certificate is genuine
```

---

## Pre-Deploy Checklist

- [ ] `DEBUG = False` in `settings.py`
- [ ] `STATIC_ROOT = BASE_DIR / "staticfiles"` added to `settings.py`
- [ ] `ALLOWED_HOSTS` includes your Render domain
- [ ] `gunicorn` added to `requirements.txt`
- [ ] `python manage.py collectstatic` ran successfully locally

---

## Troubleshooting

| Issue | Fix |
|---|---|
| Event dropdown empty on `/register/` | Go to `/admin/` → create an Event and at least one Stage first |
| `/confirm/<hash>/` shows 404 | Registration didn't complete — check that an Event exists and form submitted without errors |
| `TemplateDoesNotExist` | Confirm `'DIRS': [BASE_DIR / 'templates']` is in `settings.py` TEMPLATES |
| `get_item` filter not found | Ensure `events/templatetags/__init__.py` exists and `{% load dict_filters %}` is at top of dashboard template |
| Broken CSS/JS on Render | Add `STATIC_ROOT = BASE_DIR / "staticfiles"` to `settings.py` and run `collectstatic` |
| `DisallowedHost` error | Set `ALLOWED_HOSTS = ['*']` temporarily or add your exact Render domain |
| Application Error on Render | Check `gunicorn campusvault.wsgi` matches your actual project folder name |
| DB migrations fail | Free tier uses SQLite — fine for hackathon demos, no extra config needed |

---

## Project Structure

```
campusvault_project/
├── manage.py
├── requirements.txt
├── README.md
├── campusvault/          ← Django config package
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── events/               ← Main app
│   ├── models.py         ← Event, Stage, Participant, Attendance, Feedback
│   ├── views.py          ← All views
│   ├── forms.py          ← RegistrationForm, FeedbackForm
│   ├── urls.py           ← App URL patterns
│   ├── utils.py          ← is_eligible(), generate_pdf()
│   ├── admin.py
│   └── templatetags/
│       └── dict_filters.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── register.html
│   ├── confirm.html
│   ├── admin_dashboard.html
│   ├── feedback.html
│   └── verify.html
├── static/
│   ├── css/style.css
│   └── js/ajax_toggle.js
└── media/                ← Auto-created (receipts, QR codes)
```
