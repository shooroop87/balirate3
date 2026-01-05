# deliveries/views.py
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from .models import Shipment
from .services.dhl import DHLTrackingService, update_shipment_tracking


# deliveries/views.py
def tracking_form(request):  # Без @login_required — публичный!
    """Форма отслеживания посылки."""
    tracking_number = request.GET.get("number", "").strip()
    
    if tracking_number:
        return redirect("deliveries:tracking_detail", tracking_number=tracking_number)
    
    return render(request, "deliveries/tracking_form.html")


def tracking_detail(request, tracking_number):
    """Детали отслеживания посылки."""
    # Сначала ищем в нашей базе
    shipment = Shipment.objects.filter(tracking_number=tracking_number).first()
    
    # Получаем свежие данные от DHL
    service = DHLTrackingService()
    result = service.track(tracking_number)
    
    if not result and not shipment:
        messages.error(request, _("Sendung nicht gefunden."))
        return redirect("deliveries:tracking_form")
    
    # Если есть shipment - обновляем его
    if shipment and result:
        update_shipment_tracking(shipment)
        shipment.refresh_from_db()
    
    return render(request, "deliveries/tracking_detail.html", {
        "tracking_number": tracking_number,
        "shipment": shipment,
        "result": result,
    })


@staff_member_required
def api_update_tracking(request, shipment_id):
    """API для обновления tracking (для staff)."""
    shipment = get_object_or_404(Shipment, id=shipment_id)
    
    success = update_shipment_tracking(shipment)
    
    return JsonResponse({
        "success": success,
        "status": shipment.status if success else None,
    })