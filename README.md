# 🏛️ CampusVault
> End-to-end event and placement drive management for college campuses.

---

## 📋 Project Details

| Field | Details |
|---|---|
| **Theme** | TH-XX: Campus Event & Placement Management |
| **Team Members** | @Azmat, @Anika, @Poojitha |
| **Live URL** | *(fill after deployment)* |

---

## ✅ Submission Checklist

- [ ] Code runs with `pip install -r requirements.txt`
- [ ] `DEBUG=False` in production settings
- [ ] Working AJAX endpoint for attendance toggle (tested live)
- [ ] PDF certificate export functional
- [ ] QR code generation on registration working
- [ ] CO-SDG mapping table completed below
- [ ] 150-word SDG justification included

---

## 🎯 CO-SDG Mapping Table

| Course Outcome | How This Project Demonstrates It | SDG Target Addressed |
|---|---|---|
| CO1: MVT Architecture | CampusVault is built on Django's Model-View-Template pattern — models define Event/Participant/Attendance, views handle all logic, templates render the UI | SDG 4.5 |
| CO2: Models & Forms | Five relational models (Event, Stage, Participant, Attendance, Feedback) with validated ModelForms including file type, size, and duplicate checks | SDG 9.5 |
| CO3: AJAX & Dynamic UI | Attendance dashboard uses fetch() POST with CSRF token to toggle presence per student per stage without page reload | SDG 9.b |
| CO4: File Handling | Receipt upload with extension and size validation; QR code generation using Pillow saved to media/qrcodes/ | SDG 4.4 |
| CO5: PDF Generation | ReportLab generates Participation Certificate (FEST) or Interview Experience Letter (DRIVE) gated behind eligibility logic | SDG 8.6 |

---

## 📝 SDG Justification (150 words)

CampusVault directly advances **SDG 4 (Quality Education)** and **SDG 8 (Decent Work and Economic Growth)** by digitising the entire lifecycle of college events and placement drives. By automating registration, attendance tracking, and certificate generation, the system reduces administrative overhead and eliminates paper-based processes, making institutional record-keeping more reliable and accessible. The eligibility gating — requiring verified payment, confirmed attendance, and submitted feedback before a certificate is issued — ensures academic integrity and accountability. The QR-based certificate verification system allows employers and institutions to instantly validate participation, directly supporting SDG 8.6 by improving the credibility of student credentials. The placement drive module specifically aids students in documenting interview experience, building a verifiable portfolio of engagement. By providing a free, open-source Django template for this workflow, CampusVault enables colleges with limited resources to implement professional-grade event infrastructure, supporting SDG 4.5's goal of equal access to quality education.

---

## 📦 Setup Instructions

```bash
git clone [your-repo-url]
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

## 🔁 Full User Flow

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

## ✅ Pre-Deploy Checklist

- [ ] `DEBUG = False` in `settings.py`
- [ ] `STATIC_ROOT = BASE_DIR / "staticfiles"` added to `settings.py`
- [ ] `ALLOWED_HOSTS` includes your Render domain
- [ ] `gunicorn` added to `requirements.txt`
- [ ] `python manage.py collectstatic` ran successfully locally

---

## 🚀 Deployment Guide (Free Tier: Render)

### 1. Sign Up & Connect
- Go to [render.com](https://render.com) → Sign up with GitHub
- Authorize Render to access your repositories

### 2. Create Web Service
- Click **New +** → **Web Service** → Connect this repo
- Fill in:

| Field | Value |
|---|---|
| Name | `campusvault-app` |
| Region | Oregon or Frankfurt |
| Branch | `main` |
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --noinput` |
| Start Command | `gunicorn campusvault.wsgi` |

### 3. Environment Variables
Click **Advanced** → **Add Environment Variable**:

| Key | Value |
|---|---|
| `SECRET_KEY` | Generate at [miniwebtool.com/django-secret-key-generator](https://miniwebtool.com/django-secret-key-generator/) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `*.onrender.com,localhost,127.0.0.1` |

### 4. Deploy & Verify
- Click **Create Web Service** → wait 2–4 mins for build
- Copy your `https://....onrender.com` URL
- ✅ Test: open URL → register a student → toggle attendance → download PDF

> 💡 Every `git push` to `main` auto-triggers a rebuild. No manual restarts needed.

---

## 🚨 Troubleshooting

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

## 📁 Project Structure

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
