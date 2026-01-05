# core/services/sendpulse.py
"""
SendPulse Email Service для BlisterPerPost.
"""
import logging
from pysendpulse.pysendpulse import PySendPulse

from django.conf import settings

logger = logging.getLogger(__name__)


class SendPulseService:
    """Сервис отправки email через SendPulse API."""
    
    _instance = None
    
    @classmethod
    def get_client(cls):
        """Получить клиент SendPulse (singleton)."""
        if cls._instance is None:
            cls._instance = PySendPulse(
                settings.SENDPULSE_API_USER_ID,
                settings.SENDPULSE_API_SECRET,
                'memcached',  # или 'file' для хранения токена
            )
        return cls._instance
    
    @classmethod
    def send_email(cls, to_email, subject, html_content, text_content=None):
        """
        Отправить email.
        
        Args:
            to_email: Email получателя
            subject: Тема письма
            html_content: HTML содержимое
            text_content: Текстовое содержимое (опционально)
        
        Returns:
            bool: Успешность отправки
        """
        try:
            client = cls.get_client()
            
            email_data = {
                'html': html_content,
                'text': text_content or '',
                'subject': subject,
                'from': {
                    'name': settings.SENDPULSE_FROM_NAME,
                    'email': settings.SENDPULSE_FROM_EMAIL,
                },
                'to': [{'email': to_email}],
            }
            
            result = client.smtp_send_mail(email_data)
            
            if result and result.get('result'):
                logger.info(f"Email sent to {to_email}: {subject}")
                return True
            else:
                logger.error(f"SendPulse error: {result}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    @classmethod
    def send_verification_email(cls, user, verification_url):
        """Отправить письмо подтверждения email."""
        from django.template.loader import render_to_string
        
        subject = "Bestätigen Sie Ihre E-Mail-Adresse - BlisterPerPost"
        
        html_content = render_to_string('emails/email_verification.html', {
            'first_name': user.first_name or 'Kunde',
            'verification_url': verification_url,
        })
        
        return cls.send_email(user.email, subject, html_content)
    
    @classmethod
    def send_admin_new_user_notification(cls, user):
        """Уведомить админа о новом подтверждённом пользователе."""
        admin_email = settings.SENDPULSE_FROM_EMAIL
        subject = f"Neuer Benutzer: {user.email}"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif;">
            <h3>Neuer Benutzer registriert</h3>
            <ul>
                <li><strong>Name:</strong> {user.get_full_name() or '-'}</li>
                <li><strong>E-Mail:</strong> {user.email}</li>
                <li><strong>Telefon:</strong> {user.phone or '-'}</li>
                <li><strong>Registriert:</strong> {user.date_joined.strftime('%d.%m.%Y %H:%M')}</li>
            </ul>
        </div>
        """
        
        return cls.send_email(admin_email, subject, html_content)