from .models import Attendance
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from io import BytesIO
import math


NAVY     = colors.HexColor('#1B2A4A')
TEAL     = colors.HexColor('#2A9D8F')
GOLD     = colors.HexColor('#E9C46A')
GREY     = colors.HexColor('#6C757D')
WHITE    = colors.white


def draw_seal(c, cx, cy, radius=1.1 * cm):
    c.setStrokeColor(TEAL)
    c.setLineWidth(2.5)
    c.circle(cx, cy, radius, stroke=1, fill=0)
    c.setLineWidth(1)
    c.circle(cx, cy, radius * 0.75, stroke=1, fill=0)
    for i in range(8):
        angle = math.radians(i * 45)
        x1 = cx + math.cos(angle) * radius * 0.78
        y1 = cy + math.sin(angle) * radius * 0.78
        x2 = cx + math.cos(angle) * radius * 0.95
        y2 = cy + math.sin(angle) * radius * 0.95
        c.line(x1, y1, x2, y2)
    c.setFillColor(TEAL)
    c.setFont('Helvetica-Bold', 7)
    c.drawCentredString(cx, cy - 2.5, 'CV')


def generate_pdf(participant):
    buffer = BytesIO()
    W, H = A4
    c = canvas.Canvas(buffer, pagesize=A4)

    # Background
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Top navy bar
    c.setFillColor(NAVY)
    c.rect(0, H - 1.1 * cm, W, 1.1 * cm, fill=1, stroke=0)
    # Teal stripe below it
    c.setFillColor(TEAL)
    c.rect(0, H - 1.45 * cm, W, 0.35 * cm, fill=1, stroke=0)

    # Bottom navy bar
    c.setFillColor(NAVY)
    c.rect(0, 0, W, 1.1 * cm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, 1.1 * cm, W, 0.35 * cm, fill=1, stroke=0)

    # Gold left stripe
    c.setFillColor(GOLD)
    c.rect(0, 0, 0.4 * cm, H, fill=1, stroke=0)

    # Outer border
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.2)
    c.rect(1.1 * cm, 1.6 * cm, W - 2.2 * cm, H - 3.2 * cm, stroke=1, fill=0)

    # Inner border
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.5)
    c.rect(1.35 * cm, 1.85 * cm, W - 2.7 * cm, H - 3.7 * cm, stroke=1, fill=0)

    # Org name in top bar
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 11)
    c.drawCentredString(W / 2, H - 0.78 * cm, 'CAMPUSVAULT')

    # CERTIFICATE heading
    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 30)
    c.drawCentredString(W / 2, H - 4.5 * cm, 'CERTIFICATE')

    # Subtitle
    c.setFillColor(TEAL)
    c.setFont('Helvetica', 13)
    if participant.event.event_type == 'FEST':
        subtitle = 'O F   P A R T I C I P A T I O N'
    else:
        subtitle = 'O F   A P P R E C I A T I O N'
    c.drawCentredString(W / 2, H - 5.5 * cm, subtitle)

    # Gold rule
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(3.5 * cm, H - 6.2 * cm, W - 3.5 * cm, H - 6.2 * cm)

    # "This is to certify that"
    c.setFillColor(GREY)
    c.setFont('Helvetica', 11)
    c.drawCentredString(W / 2, H - 7.5 * cm, 'This is to certify that')

    # Participant name
    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 26)
    c.drawCentredString(W / 2, H - 8.8 * cm, participant.name.upper())

    # Underline beneath name
    name_w = c.stringWidth(participant.name.upper(), 'Helvetica-Bold', 26)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1)
    c.line(W / 2 - name_w / 2, H - 9.1 * cm,
           W / 2 + name_w / 2, H - 9.1 * cm)

    # Student ID
    c.setFillColor(GREY)
    c.setFont('Helvetica', 10)
    c.drawCentredString(W / 2, H - 9.9 * cm,
                        f'Student ID: {participant.student_id}')

    # Body sentence
    c.setFillColor(NAVY)
    c.setFont('Helvetica', 12)
    if participant.event.event_type == 'FEST':
        line1 = 'has successfully participated in'
    else:
        line1 = 'has demonstrated outstanding performance in'
    c.drawCentredString(W / 2, H - 11.0 * cm, line1)

    # Event name
    c.setFillColor(TEAL)
    c.setFont('Helvetica-Bold', 17)
    c.drawCentredString(W / 2, H - 12.0 * cm, participant.event.name)

    # Date
    c.setFillColor(GREY)
    c.setFont('Helvetica', 11)
    formatted = participant.event.date.strftime('%B %d, %Y')
    c.drawCentredString(W / 2, H - 13.0 * cm, f'held on  {formatted}')

    # Second gold rule
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(3.5 * cm, H - 13.8 * cm, W - 3.5 * cm, H - 13.8 * cm)

    # Seal bottom-left
    draw_seal(c, 5.5 * cm, H - 16.0 * cm, radius=1.1 * cm)

    # Signature line bottom-right
    sx = W - 6 * cm
    sy = H - 15.6 * cm
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.8)
    c.line(sx - 2 * cm, sy, sx + 2 * cm, sy)
    c.setFillColor(GREY)
    c.setFont('Helvetica', 8)
    c.drawCentredString(sx, sy - 0.4 * cm, 'Authorised Signatory')
    c.drawCentredString(sx, sy - 0.75 * cm, 'CampusVault')

    # Hash in bottom bar
    c.setFillColor(WHITE)
    c.setFont('Helvetica', 7)
    c.drawCentredString(W / 2, 0.38 * cm,
                        f'Verification Hash: {participant.certificate_hash}')

    c.save()
    buffer.seek(0)
    return buffer



def is_eligible(participant):
    attended = Attendance.objects.filter(
        participant=participant,
        present=True
    ).exists()

    return (
        attended and
        participant.feedback_submitted and
        participant.transaction_verified
    )




