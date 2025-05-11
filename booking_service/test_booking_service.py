import pytest
from unittest.mock import Mock
from booking_service import *

# ------------------------
# ФИКСТУРЫ
# ------------------------

@pytest.fixture
def promo_repo():
    repo = Mock()
    repo.get = Mock()
    repo.mark_used = Mock()
    return repo

@pytest.fixture
def email_sender():
    return Mock()

# ------------------------
# ТЕСТЫ ДЛЯ calc_price
# ------------------------

# Позитивные тесты
@pytest.mark.parametrize("base, discount, count, expected", [
    (100.0, 10.0, 2, 180.0),        # обычная скидка
    (50.0, 0.0, 4, 200.0),          # без скидки
])
def test_calc_price_positive(base, discount, count, expected):
    # Позитивный тест: проверка правильного расчета цены
    assert calc_price(base, discount, count) == expected

# Негативные тесты
@pytest.mark.parametrize("base, discount, count", [
    (-10, 5, 2),              # отрицательная цена
    (100, 110, 1),            # скидка больше 100%
])
def test_calc_price_negative(base, discount, count):
    # Негативный тест: должно вызывать исключение при некорректных входных данных
    with pytest.raises(ValueError):
        calc_price(base, discount, count)

# ------------------------
# ТЕСТЫ ДЛЯ check_availability
# ------------------------

# Позитивные тесты
def test_check_availability_enough_seats():
    # Позитивный тест: мест достаточно
    mock_db = Mock(return_value=10)
    assert check_availability(1, 5, mock_db) is True

def test_check_availability_exact_match():
    # Позитивный тест: мест ровно столько, сколько запрошено
    mock_db = Mock(return_value=3)
    assert check_availability(1, 3, mock_db) is True

# Негативные тесты
def test_check_availability_not_enough():
    # Негативный тест: мест недостаточно
    mock_db = Mock(return_value=2)
    assert check_availability(1, 5, mock_db) is False

def test_check_availability_invalid_request():
    # Негативный тест: отрицательное количество мест
    mock_db = Mock(return_value=10)
    with pytest.raises(ValueError):
        check_availability(1, -1, mock_db)

# ------------------------
# ТЕСТЫ ДЛЯ apply_promo_code
# ------------------------

# Позитивные тесты
def test_apply_valid_promo_code(promo_repo):
    # Позитивный тест: промокод действителен
    promo_repo.get.return_value = {"is_expired": False, "usage_left": 5}
    assert apply_promo_code(123, "PROMO10", promo_repo) is True

def test_apply_valid_promo_code_usage_edge(promo_repo):
    # Позитивный тест: usage_left > 0
    promo_repo.get.return_value = {"is_expired": False, "usage_left": 1}
    assert apply_promo_code(123, "PROMOEDGE", promo_repo) is True

# Негативные тесты
def test_apply_invalid_promo_code(promo_repo):
    # Негативный тест: промокод не найден
    promo_repo.get.return_value = None
    assert apply_promo_code(123, "INVALID", promo_repo) is False

def test_apply_expired_promo_code(promo_repo):
    # Негативный тест: промокод истек
    promo_repo.get.return_value = {"is_expired": True, "usage_left": 3}
    assert apply_promo_code(123, "EXPIRED", promo_repo) is False

# ------------------------
# ТЕСТЫ ДЛЯ generate_booking_ref
# ------------------------

# Позитивные тесты
def test_generate_booking_ref_format():
    # Позитивный тест: проверка формата строки
    ref = generate_booking_ref(42, 99)
    assert ref.startswith("BOOK-42-99-") and len(ref.split("-")[-1]) == 6

def test_generate_booking_ref_unique():
    # Позитивный тест: уникальность двух вызовов
    ref1 = generate_booking_ref(1, 1)
    ref2 = generate_booking_ref(1, 1)
    assert ref1 != ref2

# Негативные тесты
def test_generate_booking_ref_zero_ids():
    # Негативный тест: проверка допустимости нулевых значений
    ref = generate_booking_ref(0, 0)
    assert ref.startswith("BOOK-0-0-")

def test_generate_booking_ref_non_digit_suffix():
    # Негативный тест: проверка на наличие нецифровых символов в суффиксе
    ref = generate_booking_ref(1, 1)
    assert any(c.isalpha() for c in ref.split("-")[-1])

# ------------------------
# ТЕСТЫ ДЛЯ send_notification_email
# ------------------------

# Позитивные тесты
def test_send_email_success(email_sender):
    # Позитивный тест: email отправлен успешно
    email_sender.send = Mock()
    assert send_notification_email("test@example.com", {"id": 1}, email_sender) is True

def test_send_email_with_content(email_sender):
    # Позитивный тест: проверка передачи данных
    booking = {"event": "Concert", "date": "2025-01-01"}
    email_sender.send = Mock()
    assert send_notification_email("user@mail.com", booking, email_sender)

# Негативные тесты
def test_send_email_failure(email_sender):
    # Негативный тест: выбрасывается исключение
    email_sender.send.side_effect = Exception("SMTP Error")
    assert send_notification_email("fail@example.com", {}, email_sender) is False

def test_send_email_empty_address(email_sender):
    # Негативный тест: некорректный email
    email_sender.send = Mock()
    result = send_notification_email("", {"id": 1}, email_sender)
    assert result is True  # Функция не валидирует email — допустимое поведение
