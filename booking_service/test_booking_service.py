import pytest
from unittest.mock import patch
from booking_service import (
    calc_price,
    check_availability,
    apply_promo_code,
    generate_booking_ref,
    send_notification_email
)

# ==============================
# ФИКСТУРЫ
# ==============================

@pytest.fixture
def booking_details():
    return {"event": "Jazz Concert"}

@pytest.fixture
def valid_email():
    return "user@example.com"





# ==============================
# ТЕСТЫ ДЛЯ calc_price
# ==============================

# Позитивный тест: расчет без скидки
@pytest.mark.parametrize("base_price, discount, count, expected", 
                         [
                             (100, 0, 2, 200), 
                             (50, 10, 3, 135)
])
def test_calc_price_positive(base_price, discount, count, expected):
    assert calc_price(base_price, discount, count) == expected

# Негативный тест: отрицательная скидка
def test_calc_price_negative_discount():
    with pytest.raises(ValueError, match="Price and discount must be non-negative"):
        calc_price(100, -5, 2)

# Негативный тест: скидка больше 100%
def test_calc_price_negative_too_big_discount():
    with pytest.raises(ValueError, match="Discount cannot exceed 100%"):
        calc_price(100, 150, 1)

# Негативный тест: отрицательное количество билетов
def test_calc_price_negative_count():
    with pytest.raises(ValueError, match="Count must be non-negative"):
        calc_price(50, 10, -1)





# ==============================
# ТЕСТЫ ДЛЯ check_availability
# ==============================

# Позитивный тест: достаточно мест
@patch("booking_service.get_available_seats", return_value=50)
def test_check_availability_positive_enough(mock_get):
    assert check_availability(1, 20) is True

# Позитивный тест: мест точно столько, сколько нужно
@patch("booking_service.get_available_seats", return_value=10)
def test_check_availability_positive_exact(mock_get):
    assert check_availability(2, 10) is True

# Негативный тест: мест меньше, чем требуется
@patch("booking_service.get_available_seats", return_value=5)
def test_check_availability_negative_insufficient(mock_get):
    assert check_availability(3, 10) is False

# Негативный тест: запрос нуля или меньше мест
def test_check_availability_negative_invalid_request():
    with pytest.raises(ValueError, match="Requested seats must be positive"):
        check_availability(4, 0)





# ==============================
# ТЕСТЫ ДЛЯ apply_promo_code
# ==============================

# Позитивный тест: промокод валиден и не использован
@patch("booking_service.get_promo_code_data", return_value={"valid": True, "used": False})
def test_apply_promo_code_positive_valid(mock_get):
    assert apply_promo_code(1, "SUMMER2025") is True

# Позитивный тест: другой валидный промокод
@patch("booking_service.get_promo_code_data", return_value={"valid": True, "used": False})
def test_apply_promo_code_positive_another_valid(mock_get):
    assert apply_promo_code(2, "SALE50") is True

# Негативный тест: промокод использован ранее
@patch("booking_service.get_promo_code_data", return_value={"valid": True, "used": True})
def test_apply_promo_code_negative_used(mock_get):
    assert apply_promo_code(3, "EXPIRED") is False

# Негативный тест: промокод не передан
def test_apply_promo_code_negative_empty():
    with pytest.raises(ValueError, match="Promo code cannot be empty"):
        apply_promo_code(4, "")





# ==============================
# ТЕСТЫ ДЛЯ generate_booking_ref
# ==============================

# Позитивный тест: формат кода
def test_generate_booking_ref_positive_format():
    result = generate_booking_ref(10, 20)
    assert result.startswith("BOOK-10-20-") and len(result.split("-")[-1]) == 6

# Позитивный тест: уникальность кода
def test_generate_booking_ref_positive_unique():
    ref1 = generate_booking_ref(1, 1)
    ref2 = generate_booking_ref(1, 1)
    assert ref1 != ref2

# Негативный тест: user_id <= 0
def test_generate_booking_ref_negative_user():
    with pytest.raises(ValueError, match="IDs must be positive"):
        generate_booking_ref(0, 10)

# Негативный тест: event_id <= 0
def test_generate_booking_ref_negative_event():
    with pytest.raises(ValueError, match="IDs must be positive"):
        generate_booking_ref(10, 0)

# ==============================
# ТЕСТЫ ДЛЯ send_notification_email
# ==============================

# Позитивный тест: успешная отправка письма
@patch("booking_service.send_email", return_value=True)
def test_send_notification_email_positive(mock_send, valid_email, booking_details):
    assert send_notification_email(valid_email, booking_details) is True

# Позитивный тест: другая бронь, email корректный
@patch("booking_service.send_email", return_value=True)
def test_send_notification_email_positive_other(mock_send):
    assert send_notification_email("client@example.org", {"event": "Theatre"}) is True

# Негативный тест: некорректный email
def test_send_notification_email_negative_email():
    with pytest.raises(ValueError, match="Invalid email"):
        send_notification_email("bademail", {"event": "X"})

# Негативный тест: сбой в отправке письма
@patch("booking_service.send_email", return_value=False)
def test_send_notification_email_negative_smtp(mock_send):
    result = send_notification_email("user@example.com", {"event": "Concert"})
    assert result is False
