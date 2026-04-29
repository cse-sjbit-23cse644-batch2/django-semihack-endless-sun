from django import forms
from .models import Participant, Feedback
import os


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['student_id', 'name', 'email', 'event', 'transaction_id', 'receipt']
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 22CS001'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'college@email.com'
            }),
            'event': forms.Select(attrs={
                'class': 'form-select'
            }),
            'transaction_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UPI / bank transaction ID'
            }),
            'receipt': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_transaction_id(self):
        transaction_id = self.cleaned_data.get('transaction_id')
        # On edit, exclude current instance from duplicate check
        qs = Participant.objects.filter(transaction_id=transaction_id)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This transaction ID is already registered.")
        return transaction_id

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        qs = Participant.objects.filter(student_id=student_id)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This student ID is already registered.")
        return student_id

    def clean_receipt(self):
        receipt = self.cleaned_data.get('receipt')
        if receipt:
            # File size check — max 2MB
            if receipt.size > 2 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 2MB.")
            # File type check
            ext = os.path.splitext(receipt.name)[1].lower()
            allowed = ['.pdf', '.png', '.jpg', '.jpeg']
            if ext not in allowed:
                raise forms.ValidationError("Only PDF, PNG, JPG files are allowed.")
        return receipt
    


class FeedbackForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience...'
            }),
        }