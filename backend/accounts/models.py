from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom manager для User с email вместо username."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("E-Mail ist erforderlich"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model для Balirate."""

    username = None
    email = models.EmailField(_("E-Mail-Adresse"), unique=True)

    # Персональные данные
    phone = models.CharField(_("Telefonnummer"), max_length=20, blank=True)
    date_of_birth = models.DateField(_("Geburtsdatum"), null=True, blank=True)

    # Адрес доставки
    street = models.CharField(_("Straße und Hausnummer"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postleitzahl"), max_length=10, blank=True)
    city = models.CharField(_("Stadt"), max_length=100, blank=True)
    country = models.CharField(
        _("Land"),
        max_length=2,
        choices=[("DE", "Deutschland"), ("AT", "Österreich")],
        default="DE",
    )

    # Медицинская информация
    insurance_number = models.CharField(
        _("Versichertennummer"), max_length=20, blank=True
    )
    insurance_company = models.CharField(
        _("Krankenkasse"), max_length=100, blank=True
    )

    # Настройки
    language = models.CharField(
        _("Sprache"),
        max_length=2,
        choices=[("de", "Deutsch"), ("en", "English")],
        default="de",
    )

    # ===========================================
    # DSGVO Einwilligungen (с датами для аудита)
    # ===========================================
    
    # AGB
    terms_accepted = models.BooleanField(
        _("AGB akzeptiert"), default=False
    )
    terms_accepted_at = models.DateTimeField(
        _("AGB akzeptiert am"), null=True, blank=True
    )
    
    # Datenschutzerklärung
    privacy_accepted = models.BooleanField(
        _("Datenschutz akzeptiert"), default=False
    )
    privacy_accepted_at = models.DateTimeField(
        _("Datenschutz akzeptiert am"), null=True, blank=True
    )
    
    # Art. 9 DSGVO - Gesundheitsdaten
    medical_data_consent = models.BooleanField(
        _("Einwilligung Gesundheitsdaten"), default=False
    )
    medical_data_consent_at = models.DateTimeField(
        _("Einwilligung Gesundheitsdaten am"), null=True, blank=True
    )
    
    # Marketing / Newsletter
    marketing_consent = models.BooleanField(
        _("Marketing-Einwilligung"), default=False
    )
    marketing_consent_at = models.DateTimeField(
        _("Marketing-Einwilligung am"), null=True, blank=True
    )

    # Legacy field (für Abwärtskompatibilität)
    data_processing_consent = models.BooleanField(
        _("Einwilligung zur Datenverarbeitung"), default=False
    )

    # ===========================================
    # Payment Provider
    # ===========================================
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    paypal_payer_id = models.CharField(
        _("PayPal Payer ID"), max_length=100, blank=True
    )

    # ===========================================
    # Onboarding Status
    # ===========================================
    class OnboardingStep(models.IntegerChoices):
        PROFILE = 1, _("Profil ausfüllen")
        DOCUMENTS = 2, _("Dokumente hochladen")
        PLAN = 3, _("Tarif wählen")
        PAYMENT = 4, _("Zahlung einrichten")
        COMPLETED = 5, _("Abgeschlossen")

    onboarding_step = models.IntegerField(
        _("Onboarding-Schritt"),
        choices=OnboardingStep.choices,
        default=1,
    )
    onboarding_completed = models.BooleanField(
        _("Onboarding abgeschlossen"), default=False
    )
    documents_verified = models.BooleanField(
        _("Dokumente geprüft"), default=False
    )

    # Метаданные
    created_at = models.DateTimeField(_("Erstellt am"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Aktualisiert am"), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("Benutzer")
        verbose_name_plural = _("Benutzer")
        ordering = ["-created_at"]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    @property
    def full_address(self):
        parts = [self.street, f"{self.postal_code} {self.city}".strip()]
        return ", ".join(filter(None, parts))
    
    @property
    def has_active_subscription(self):
        return self.subscriptions.filter(status__in=["active", "trialing"]).exists()
    
    @property
    def has_all_consents(self):
        """Проверяет, есть ли все обязательные согласия."""
        return all([
            self.terms_accepted,
            self.privacy_accepted,
            self.medical_data_consent,
        ])

    def is_profile_complete(self):
        """Проверяет заполнен ли профиль полностью."""
        required_fields = [
            self.first_name, self.last_name, self.phone,
            self.date_of_birth, self.street, self.postal_code, self.city
        ]
        return all(required_fields)


class UserDocument(models.Model):
    """Загруженные документы пользователя."""

    class DocumentType(models.TextChoices):
        PRESCRIPTION = "prescription", _("Rezept")
        INSURANCE_CARD = "insurance_card", _("Versichertenkarte")
        ID_DOCUMENT = "id_document", _("Ausweisdokument")
        OTHER = "other", _("Sonstiges")

    class Status(models.TextChoices):
        PENDING = "pending", _("Ausstehend")
        APPROVED = "approved", _("Genehmigt")
        REJECTED = "rejected", _("Abgelehnt")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Benutzer"),
    )
    document_type = models.CharField(
        _("Dokumenttyp"),
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.PRESCRIPTION,
    )
    file = models.FileField(_("Datei"), upload_to="documents/%Y/%m/")
    original_filename = models.CharField(_("Originaldateiname"), max_length=255)
    description = models.TextField(_("Beschreibung"), blank=True)
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    reviewed_at = models.DateTimeField(_("Überprüft am"), null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_documents",
    )
    rejection_reason = models.TextField(_("Ablehnungsgrund"), blank=True)

    created_at = models.DateTimeField(_("Hochgeladen am"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Aktualisiert am"), auto_now=True)

    class Meta:
        verbose_name = _("Dokument")
        verbose_name_plural = _("Dokumente")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.user.email}"


class ConsentLog(models.Model):
    """Логирование согласий DSGVO - неизменяемый аудит."""
    
    class ConsentType(models.TextChoices):
        MEDICAL_DATA = "medical_data", _("Medizinische Daten (Art. 9 DSGVO)")
        TERMS = "terms", _("AGB")
        PRIVACY = "privacy", _("Datenschutzerklärung")
        MARKETING = "marketing", _("Marketing")
        COOKIES_FUNCTIONAL = "cookies_functional", _("Funktionale Cookies")
        COOKIES_ANALYTICS = "cookies_analytics", _("Analyse-Cookies")
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="consent_logs",
        verbose_name=_("Benutzer"),
        null=True,
        blank=True,
    )
    
    consent_type = models.CharField(
        _("Art der Einwilligung"),
        max_length=30,
        choices=ConsentType.choices,
    )
    
    granted = models.BooleanField(_("Erteilt"), default=True)
    
    consent_version = models.CharField(
        _("Version der Einwilligung"),
        max_length=20,
        default="1.0",
    )
    
    ip_address = models.GenericIPAddressField(_("IP-Adresse"), null=True, blank=True)
    user_agent = models.TextField(_("User Agent"), blank=True)
    
    consent_text_hash = models.CharField(
        _("Hash des Einwilligungstexts"),
        max_length=64,
        blank=True,
        help_text=_("SHA256 hash для проверки изменений текста")
    )
    
    created_at = models.DateTimeField(_("Erteilt am"), auto_now_add=True)
    withdrawn_at = models.DateTimeField(_("Widerrufen am"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Einwilligungsprotokoll")
        verbose_name_plural = _("Einwilligungsprotokolle")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "consent_type"]),
            models.Index(fields=["consent_type", "created_at"]),
        ]
    
    def __str__(self):
        status = "✓" if self.granted and not self.withdrawn_at else "✗"
        return f"{status} {self.get_consent_type_display()} - {self.user or 'Anonym'}"
    
    @property
    def is_active(self):
        return self.granted and self.withdrawn_at is None