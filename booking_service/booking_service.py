import random
import string
from datetime import datetime

# Функция 1: calc_price
def calc_price(base_price: float, discount: float, count: int) -> float:
    """
    Рассчитывает итоговую сумму за указанное количество билетов с учетом скидки.
    """
    if count < 0 or base_price < 0:
        raise ValueError("Некорректное количество билетов или цена")
    if discount < 0 or discount > 100:
        raise ValueError("Скидка должна быть в пределах от 0 до 100%")

    final_price = base_price * (1 - discount / 100) * count
    return round(final_price, 2)

# Функция 2: check_availability
def check_availability(event_id: int, seats_requested: int, db_lookup) -> bool:
    """
    Проверяет наличие свободных мест на мероприятие, используя внешнюю функцию db_lookup для получения доступных мест.
    """
    if seats_requested <= 0:
        raise ValueError("Запрошено некорректное количество мест")
    available_seats = db_lookup(event_id)
    return seats_requested <= available_seats

# Функция 3: apply_promo_code
def apply_promo_code(order_id: int, promo_code: str, promo_repo) -> bool:
    """
    Применяет промокод к заказу, если он действителен и доступен.
    """
    promo = promo_repo.get(promo_code)
    if not promo or promo["is_expired"] or promo["usage_left"] <= 0:
        return False
    promo_repo.mark_used(promo_code)
    return True

# Функция 4: generate_booking_ref
def generate_booking_ref(user_id: int, event_id: int) -> str:
    """
    Генерирует уникальный код бронирования вида BOOK-<user_id>-<event_id>-<случайный_хвост>
    """
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"BOOK-{user_id}-{event_id}-{suffix}"

# Функция 5: send_notification_email
def send_notification_email(email: str, booking_details: dict, email_sender) -> bool:
    """
    Отправляет email с деталями бронирования, используя переданный email_sender.
    """
    try:
        email_sender.send(email, booking_details)
        return True
    except Exception:
        return False
