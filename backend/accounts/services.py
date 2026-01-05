# backend/accounts/services.py (новый файл)
import hashlib
from django.utils import timezone


class ConsentService:
    """Сервис для работы с согласиями DSGVO."""
    
    # Версии текстов (менять при изменении consent.html и т.д.)
    VERSIONS = {
        "medical_data": "1.0",
        "terms": "1.0",
        "privacy": "1.0",
        "marketing": "1.0",
        "cookies_functional": "1.0",
        "cookies_analytics": "1.0",
    }
    
    @classmethod
    def log_consent(cls, consent_type, granted, user=None, request=None):
        """
        Записать согласие в БД.
        
        Args:
            consent_type: тип согласия (из ConsentLog.ConsentType)
            granted: True/False
            user: пользователь (может быть None для cookies)
            request: HTTP request для IP и User-Agent
        """
        from accounts.models import ConsentLog
        
        ip_address = None
        user_agent = ""
        
        if request:
            ip_address = cls._get_client_ip(request)
            user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
        
        return ConsentLog.objects.create(
            user=user,
            consent_type=consent_type,
            granted=granted,
            consent_version=cls.VERSIONS.get(consent_type, "1.0"),
            ip_address=ip_address,
            user_agent=user_agent,
            consent_text_hash=cls._get_consent_hash(consent_type),
        )
    
    @classmethod
    def withdraw_consent(cls, user, consent_type):
        """Отозвать согласие."""
        from accounts.models import ConsentLog
        
        # Находим активное согласие
        active = ConsentLog.objects.filter(
            user=user,
            consent_type=consent_type,
            granted=True,
            withdrawn_at__isnull=True,
        ).first()
        
        if active:
            active.withdrawn_at = timezone.now()
            active.save(update_fields=["withdrawn_at"])
            return active
        return None
    
    @classmethod
    def has_active_consent(cls, user, consent_type):
        """Проверить есть ли активное согласие."""
        from accounts.models import ConsentLog
        
        return ConsentLog.objects.filter(
            user=user,
            consent_type=consent_type,
            granted=True,
            withdrawn_at__isnull=True,
        ).exists()
    
    @classmethod
    def get_user_consents(cls, user):
        """Получить все активные согласия пользователя."""
        from accounts.models import ConsentLog
        
        return ConsentLog.objects.filter(
            user=user,
            granted=True,
            withdrawn_at__isnull=True,
        ).values_list("consent_type", flat=True)
    
    @classmethod
    def log_registration_consents(cls, user, request, consents_dict):
        """
        Записать все согласия при регистрации.
        
        consents_dict = {
            "medical_data": True,
            "terms": True,
            "privacy": True,
            "marketing": False,
        }
        """
        logs = []
        for consent_type, granted in consents_dict.items():
            log = cls.log_consent(
                consent_type=consent_type,
                granted=granted,
                user=user,
                request=request,
            )
            logs.append(log)
        return logs
    
    @staticmethod
    def _get_client_ip(request):
        """Получить IP клиента."""
        x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded:
            return x_forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
    
    @staticmethod
    def _get_consent_hash(consent_type):
        """Хеш текста согласия (упрощённо — версия)."""
        # В идеале — хешировать реальный текст из шаблона
        version = ConsentService.VERSIONS.get(consent_type, "1.0")
        return hashlib.sha256(f"{consent_type}:{version}".encode()).hexdigest()[:16]