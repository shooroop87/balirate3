from django.shortcuts import redirect
from django.urls import reverse, resolve
from django.http import Http404


class OnboardingMiddleware:
    """Проверяет прошёл ли пользователь онбординг."""
    
    EXEMPT_PATHS = [
        '/admin/',
        '/account/logout/',
        '/account/login/',
        '/account/signup/',
        '/account/onboarding/',
        '/static/',
        '/media/',
        '/__reload__/',
        '/set-language/',
        '/webhooks/',
        '/account/google/',
        '/account/social/',
        '/account/confirm-email/',
        '/account/password/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пропускаем неаутентифицированных и staff
        if not request.user.is_authenticated or request.user.is_staff:
            return self.get_response(request)
        
        path = request.path
        
        # Пропускаем исключённые пути
        if any(path.startswith(exempt) for exempt in self.EXEMPT_PATHS):
            return self.get_response(request)
        
        # Проверяем онбординг
        user = request.user
        if not user.onboarding_completed:
            step = user.onboarding_step
            
            # Маппинг шагов на URL
            step_urls = {
                1: 'onboarding_profile',
                2: 'onboarding_documents',
                3: 'onboarding_plan',
                4: 'onboarding_payment',
            }
            
            target_name = step_urls.get(step, 'onboarding_profile')
            
            try:
                target_url = reverse(target_name)
            except Exception:
                target_url = reverse('onboarding_profile')
            
            # Редирект если не на странице онбординга
            if not path.startswith('/account/onboarding/'):
                return redirect(target_url)
        
        return self.get_response(request)