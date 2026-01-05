# deliveries/services/dhl.py
"""
DHL Unified API Integration.

API Docs: https://developer.dhl.com/api-reference/shipment-tracking
"""
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import requests
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


@dataclass
class TrackingEvent:
    """Событие отслеживания."""
    timestamp: datetime
    location: str
    status_code: str
    description: str
    
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "location": self.location,
            "status_code": self.status_code,
            "description": self.description,
        }


@dataclass
class TrackingResult:
    """Результат отслеживания."""
    tracking_number: str
    status: str
    status_code: str
    origin: Optional[str]
    destination: Optional[str]
    estimated_delivery: Optional[datetime]
    actual_delivery: Optional[datetime]
    events: list[TrackingEvent]
    raw_data: dict


class DHLTrackingService:
    """Сервис отслеживания посылок DHL."""
    
    BASE_URL = "https://api-eu.dhl.com/track/shipments"
    
    # Маппинг статусов DHL на наши статусы
    STATUS_MAP = {
        "pre-transit": "label_created",
        "transit": "in_transit",
        "out-for-delivery": "out_for_delivery",
        "delivered": "delivered",
        "failure": "failed",
        "return": "returned",
        "unknown": "in_transit",
    }
    
    def __init__(self):
        self.api_key = settings.DHL_API_KEY
        self.headers = {
            "DHL-API-Key": self.api_key,
            "Accept": "application/json",
        }
    
    def track(self, tracking_number: str) -> Optional[TrackingResult]:
        """
        Получить информацию о посылке по номеру отслеживания.
        
        Args:
            tracking_number: Номер отслеживания DHL
            
        Returns:
            TrackingResult или None если не найдено
        """
        try:
            response = requests.get(
                self.BASE_URL,
                headers=self.headers,
                params={"trackingNumber": tracking_number},
                timeout=10,
            )
            
            if response.status_code == 404:
                logger.warning(f"Tracking number not found: {tracking_number}")
                return None
            
            response.raise_for_status()
            data = response.json()
            
            return self._parse_response(tracking_number, data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"DHL API error for {tracking_number}: {e}")
            return None
    
    def _parse_response(self, tracking_number: str, data: dict) -> Optional[TrackingResult]:
        """Парсинг ответа DHL API."""
        shipments = data.get("shipments", [])
        
        if not shipments:
            return None
        
        shipment = shipments[0]
        
        # Парсим события
        events = []
        for event_data in shipment.get("events", []):
            event = self._parse_event(event_data)
            if event:
                events.append(event)
        
        # Сортируем по времени (новые первые)
        events.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Определяем статус
        status_info = shipment.get("status", {})
        status_code = status_info.get("statusCode", "unknown")
        status = self.STATUS_MAP.get(status_code, "in_transit")
        
        # Даты
        estimated_delivery = None
        if shipment.get("estimatedTimeOfDelivery"):
            try:
                estimated_delivery = datetime.fromisoformat(
                    shipment["estimatedTimeOfDelivery"].replace("Z", "+00:00")
                )
            except ValueError:
                pass
        
        actual_delivery = None
        if status == "delivered" and events:
            actual_delivery = events[0].timestamp
        
        # Адреса
        origin = None
        destination = None
        
        if shipment.get("origin"):
            origin_data = shipment["origin"].get("address", {})
            origin = f"{origin_data.get('addressLocality', '')}, {origin_data.get('countryCode', '')}"
        
        if shipment.get("destination"):
            dest_data = shipment["destination"].get("address", {})
            destination = f"{dest_data.get('addressLocality', '')}, {dest_data.get('countryCode', '')}"
        
        return TrackingResult(
            tracking_number=tracking_number,
            status=status,
            status_code=status_code,
            origin=origin,
            destination=destination,
            estimated_delivery=estimated_delivery,
            actual_delivery=actual_delivery,
            events=events,
            raw_data=data,
        )
    
    def _parse_event(self, event_data: dict) -> Optional[TrackingEvent]:
        """Парсинг события."""
        try:
            timestamp = datetime.fromisoformat(
                event_data["timestamp"].replace("Z", "+00:00")
            )
            
            location_data = event_data.get("location", {}).get("address", {})
            location = location_data.get("addressLocality", "")
            if location_data.get("countryCode"):
                location = f"{location}, {location_data['countryCode']}"
            
            return TrackingEvent(
                timestamp=timestamp,
                location=location or "Unknown",
                status_code=event_data.get("statusCode", ""),
                description=event_data.get("description", ""),
            )
        except (KeyError, ValueError) as e:
            logger.warning(f"Failed to parse DHL event: {e}")
            return None


class DHLShippingService:
    """Сервис создания отправлений DHL (Business API)."""
    
    # Для production нужен DHL Business Customer Portal
    BASE_URL = "https://api-eu.dhl.com/parcel/de/shipping/v2"
    
    def __init__(self):
        self.api_key = settings.DHL_API_KEY
        self.api_secret = settings.DHL_API_SECRET
        self.account_number = getattr(settings, "DHL_ACCOUNT_NUMBER", "")
    
    def create_shipment(
        self,
        sender: dict,
        recipient: dict,
        weight: float,  # kg
        reference: str = "",
    ) -> Optional[dict]:
        """
        Создать отправление и получить этикетку.
        
        Args:
            sender: Данные отправителя
            recipient: Данные получателя
            weight: Вес в кг
            reference: Референс (номер заказа)
            
        Returns:
            dict с tracking_number и label_url или None
        """
        # Это пример структуры - реальная интеграция требует
        # DHL Business Customer Portal и другие credentials
        
        payload = {
            "profile": "STANDARD_GRUPPENPROFIL",
            "shipments": [{
                "product": "V01PAK",  # DHL Paket
                "billingNumber": self.account_number,
                "refNo": reference,
                "shipper": {
                    "name1": sender.get("name", ""),
                    "addressStreet": sender.get("street", ""),
                    "postalCode": sender.get("postal_code", ""),
                    "city": sender.get("city", ""),
                    "country": sender.get("country", "DEU"),
                },
                "consignee": {
                    "name1": recipient.get("name", ""),
                    "addressStreet": recipient.get("street", ""),
                    "postalCode": recipient.get("postal_code", ""),
                    "city": recipient.get("city", ""),
                    "country": recipient.get("country", "DEU"),
                },
                "details": {
                    "weight": {
                        "uom": "kg",
                        "value": weight,
                    }
                }
            }]
        }
        
        try:
            response = requests.post(
                f"{self.BASE_URL}/orders",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Basic {self._get_auth()}",
                },
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            
            # Парсим результат
            items = data.get("items", [])
            if items and items[0].get("shipmentNo"):
                return {
                    "tracking_number": items[0]["shipmentNo"],
                    "label_url": items[0].get("label", {}).get("url"),
                    "label_data": items[0].get("label", {}).get("b64"),
                }
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"DHL Shipping API error: {e}")
            return None
    
    def _get_auth(self) -> str:
        """Получить Basic Auth строку."""
        import base64
        credentials = f"{self.api_key}:{self.api_secret}"
        return base64.b64encode(credentials.encode()).decode()


def update_shipment_tracking(shipment) -> bool:
    """
    Обновить статус отслеживания для Shipment.
    
    Args:
        shipment: объект Shipment из deliveries.models
        
    Returns:
        True если обновлено, False если ошибка
    """
    from deliveries.models import Shipment
    
    if not shipment.tracking_number:
        return False
    
    service = DHLTrackingService()
    result = service.track(shipment.tracking_number)
    
    if not result:
        return False
    
    # Обновляем статус
    status_map = {
        "label_created": Shipment.Status.LABEL_CREATED,
        "picked_up": Shipment.Status.PICKED_UP,
        "in_transit": Shipment.Status.IN_TRANSIT,
        "out_for_delivery": Shipment.Status.OUT_FOR_DELIVERY,
        "delivered": Shipment.Status.DELIVERED,
        "failed": Shipment.Status.FAILED,
        "returned": Shipment.Status.RETURNED,
    }
    
    new_status = status_map.get(result.status, Shipment.Status.IN_TRANSIT)
    
    # Обновляем поля
    shipment.status = new_status
    shipment.tracking_events = [e.to_dict() for e in result.events]
    
    if result.estimated_delivery:
        shipment.estimated_delivery = result.estimated_delivery
    
    if result.actual_delivery:
        shipment.actual_delivery = result.actual_delivery
        
        # Обновляем связанный заказ
        if hasattr(shipment, "order") and shipment.order:
            from deliveries.models import BlisterOrder
            shipment.order.status = BlisterOrder.Status.DELIVERED
            shipment.order.delivered_at = result.actual_delivery
            shipment.order.save()
    
    shipment.save()
    
    logger.info(f"Updated shipment {shipment.id} tracking: {new_status}")
    return True