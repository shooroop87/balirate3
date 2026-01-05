from django.conf import settings
from django.utils import translation


class StrictLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем язык из заголовка запроса, куки или URL (например, /fr/)
        lang = translation.get_language_from_request(request)

        # Берём список поддерживаемых языков из настроек
        supported = dict(settings.LANGUAGES)

        if lang not in supported:
            # Если язык не поддерживается — насильно включаем язык по умолчанию
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        else:
            # Если поддерживается — активируем этот язык
            translation.activate(lang)
            request.LANGUAGE_CODE = lang

        # Продолжаем выполнение запроса
        return self.get_response(request)
