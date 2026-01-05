# accounts/adapters.py
"""
Custom Allauth Adapter для HTML emails через Django SMTP.
"""
import logging

from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


class HTMLEmailAccountAdapter(DefaultAccountAdapter):
    """
    Adapter который отправляет красивые HTML письма.
    """
    
    def send_mail(self, template_prefix, email, context):
        """
        Отправляем HTML email.
        """
        logger.info(f"HTMLEmailAccountAdapter: {template_prefix} -> {email}")
        
        # Тема
        subject = render_to_string(f'{template_prefix}_subject.txt', context)
        subject = " ".join(subject.splitlines()).strip()
        
        # HTML
        html_body = render_to_string(f'{template_prefix}_message.html', context)
        
        # Отправляем
        msg = EmailMultiAlternatives(
            subject=subject,
            body="",  # пустой text body
            from_email=None,
            to=[email]
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()
        
        logger.info(f"Email sent to {email}")