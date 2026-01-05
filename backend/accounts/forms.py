# backend/accounts/forms.py
from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import SignupForm

from deliveries.models import Medication
from .models import User, UserDocument


class CustomSignupForm(SignupForm):
    """Форма регистрации с DSGVO согласиями."""
    
    first_name = forms.CharField(
        label=_("Vorname"),
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label=_("Nachname"),
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    
    terms_accepted = forms.BooleanField(
        label=_("Ich akzeptiere die AGB"),
        required=True,
        error_messages={"required": _("Sie müssen die AGB akzeptieren.")},
    )
    privacy_accepted = forms.BooleanField(
        label=_("Ich akzeptiere die Datenschutzerklärung"),
        required=True,
        error_messages={"required": _("Sie müssen die Datenschutzerklärung akzeptieren.")},
    )
    medical_consent = forms.BooleanField(
        label=_("Einwilligung zur Verarbeitung von Gesundheitsdaten (Art. 9 DSGVO)"),
        required=True,
        error_messages={"required": _("Diese Einwilligung ist für unseren Service erforderlich.")},
    )
    marketing_consent = forms.BooleanField(
        label=_("Newsletter erhalten"),
        required=False,
    )

    def save(self, request):
        user = super().save(request)
        from .services import ConsentService
        now = timezone.now()
        
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.terms_accepted = True
        user.terms_accepted_at = now
        user.privacy_accepted = True
        user.privacy_accepted_at = now
        user.medical_data_consent = True
        user.medical_data_consent_at = now
        
        if self.cleaned_data.get("marketing_consent"):
            user.marketing_consent = True
            user.marketing_consent_at = now
        
        user.save()
        ConsentService.log_registration_consents(
            user=user, request=request,
            consents_dict={"terms": True, "privacy": True, "medical_data": True,
                      "marketing": self.cleaned_data.get("marketing_consent", False)}
        )
        return user
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "date_of_birth", "language"]
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date", "class": "form-control"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = "form-control"


class AddressForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["street", "postal_code", "city", "country"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class InsuranceForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["insurance_number", "insurance_company"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = UserDocument
        fields = ["document_type", "file", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["file"].widget.attrs["accept"] = ".pdf,.jpg,.jpeg,.png"


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ["name", "dosage", "pzn", "morning", "noon", "evening", "night", "instructions"]
        widgets = {"instructions": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super().clean()
        if not any(cleaned_data.get(t) for t in ["morning", "noon", "evening", "night"]):
            raise forms.ValidationError(_("Bitte wählen Sie mindestens einen Einnahmezeitpunkt."))
        return cleaned_data


class ContactForm(forms.Form):
    name = forms.CharField(label=_("Name"), max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label=_("E-Mail"), widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone = forms.CharField(label=_("Telefon"), max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    subject = forms.ChoiceField(
        label=_("Betreff"),
        choices=[("", _("Bitte wählen")), ("general", _("Allgemeine Anfrage")), ("order", _("Frage zur Bestellung")),
                 ("delivery", _("Lieferung & Versand")), ("prescription", _("Rezept-Fragen")),
                 ("technical", _("Technische Probleme")), ("complaint", _("Beschwerde")), ("other", _("Sonstiges"))],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    message = forms.CharField(label=_("Nachricht"), widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))
    privacy = forms.BooleanField(label=_("Ich habe die Datenschutzerklärung gelesen und akzeptiere sie."),
                                  widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))