import random
import string
from typing import Dict

# ===== МОКИРУЕМЫЕ ЗАВИСИМОСТИ =====

def get_available_seats(event_id: int) -> int:
    """
    Возвращает количество доступных мест на мероприятии (мокается в тестах).
    """
    return 100

def get_promo_code_data(promo_code: str) -> Dict:
    """
    Возвращает информацию о промокоде (валидность, лимит, срок действия).
    """
    return {"valid": True, "used": False}

def send_email(email: str, content: str) -> bool:
    """
    Отправляет email-уведомление (мокается в тестах).
    """
    return True

# ===== ОСНОВНЫЕ ФУНКЦИИ BOOKING-СЕРВИСА =====

def calc_price(base_price: float, discount: float, count: int) -> float:
    """
    Рассчитывает итоговую цену за count билетов с учетом скидки.
    Проверки:
    - base_price >= 0, discount >= 0
    - count >= 0
    - скидка не больше 100%
    """
    if base_price < 0 or discount < 0:
        raise ValueError("Price and discount must be non-negative.")
    if discount > 100:
        raise ValueError("Discount cannot exceed 100%.")
    if count < 0:
        raise ValueError("Count must be non-negative.")
    final_price = base_price * (1 - discount / 100) * count
    return round(final_price, 2)

def check_availability(event_id: int, seats_requested: int) -> bool:
    """
    Проверяет, есть ли достаточно мест на событие.
    Использует get_available_seats() — можно мокировать.
    """
    if seats_requested <= 0:
        raise ValueError("Requested seats must be positive.")
    available = get_available_seats(event_id)
    return seats_requested <= available

def apply_promo_code(order_id: int, promo_code: str) -> bool:
    """
    Применяет промокод к заказу, если он действителен.
    Использует get_promo_code_data() — можно мокировать.
    """
    if not promo_code:
        raise ValueError("Promo code cannot be empty.")
    data = get_promo_code_data(promo_code)
    return data.get("valid") and not data.get("used")

def generate_booking_ref(user_id: int, event_id: int) -> str:
    """
    Генерирует уникальный код бронирования: BOOK-<user_id>-<event_id>-<SUFFIX>
    """
    if user_id <= 0 or event_id <= 0:
        raise ValueError("IDs must be positive.")
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"BOOK-{user_id}-{event_id}-{suffix}"

def send_notification_email(email: str, booking_details: Dict) -> bool:
    """
    Отправляет email-уведомление о бронировании. Использует send_email().
    Проверяет email, вызывает внешний сервис — мокаем.
    """
    if "@" not in email:
        raise ValueError("Invalid email.")
    content = f"Booking confirmed for event: {booking_details.get('event')}"
    return send_email(email, content)
