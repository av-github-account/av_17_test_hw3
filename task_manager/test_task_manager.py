import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from task_manager import (
    create_task,
    track_time,
    calculate_invoice,
    check_project_deadline,
    send_task_notification
)

# ===== Фикстуры =====
@pytest.fixture
def future_deadline():
    return datetime.now() + timedelta(days=5)

@pytest.fixture
def valid_email():
    return "user@example.com"

@pytest.fixture
def task_info():
    return {"title": "Задача A", "status": "создана"}

# ===== Тесты create_task =====
@pytest.mark.parametrize("project_id, title", [(1, "Task 1"), (10, "Задача B")])
def test_create_task_positive(project_id, title, future_deadline):
    # Позитивный тест: корректное создание задачи
    result = create_task(project_id, title, future_deadline)
    assert isinstance(result, int)

def test_create_task_negative_empty_title(future_deadline):
    # Негативный тест: пустой заголовок задачи
    with pytest.raises(ValueError, match="Title cannot be empty."):
        create_task(1, "", future_deadline)

def test_create_task_negative_past_deadline():
    # Негативный тест: дедлайн в прошлом
    past = datetime.now() - timedelta(days=1)
    with pytest.raises(ValueError, match="Deadline cannot be in the past."):
        create_task(1, "Title", past)

def test_create_task_negative_invalid_project(future_deadline):
    # Негативный тест: project_id некорректный
    with pytest.raises(ValueError, match="Invalid project ID."):
        create_task(0, "Title", future_deadline)

# ===== Тесты track_time =====
@pytest.mark.parametrize("task_id, hours", [(1, 5.5), (10, 1000.0)])
def test_track_time_positive(task_id, hours):
    # Позитивный тест: корректное добавление времени
    result = track_time(task_id, hours)
    assert result == hours

# Позитивный тест: минимальное допустимое значение часов (>0)
def test_track_time_positive_minimal_hours():
    result = track_time(1, 0.01)
    assert result == 0.01
    
def test_track_time_negative_zero_hours():
    # Негативный тест: 0 часов
    with pytest.raises(ValueError, match="Hours must be positive."):
        track_time(1, 0)

def test_track_time_negative_negative_hours():
    # Негативный тест: отрицательные часы
    with pytest.raises(ValueError, match="Hours must be positive."):
        track_time(1, -3.0)

def test_track_time_negative_too_many_hours():
    # Негативный тест: слишком много часов
    with pytest.raises(ValueError, match="Unrealistic number of hours."):
        track_time(1, 1001)

# ===== Тесты calculate_invoice =====
@pytest.mark.parametrize("hours, rate, currency, expected", [
    (10, 50, "USD", 500.0),
    (2.5, 100, "EUR", 250.0),
])
def test_calculate_invoice_positive(hours, rate, currency, expected):
    # Позитивный тест: корректный расчет счета
    assert calculate_invoice(hours, rate, currency) == expected

def test_calculate_invoice_negative_unsupported_currency():
    # Негативный тест: неподдерживаемая валюта
    with pytest.raises(ValueError, match="Unsupported currency."):
        calculate_invoice(5, 10, "RUB")

def test_calculate_invoice_negative_negative_hours():
    # Негативный тест: отрицательные часы
    with pytest.raises(ValueError, match="Hours and rate must be non-negative."):
        calculate_invoice(-1, 10, "USD")

def test_calculate_invoice_negative_zero_rate():
    # Негативный тест: ставка 0 (но валидно, результат — 0)
    assert calculate_invoice(10, 0, "EUR") == 0.0

# ===== Тесты check_project_deadline =====
@patch("task_manager.get_project_deadline", return_value=datetime(2025, 5, 15))
@patch("task_manager.datetime")
def test_check_project_deadline_positive(mock_datetime, mock_get_deadline):
    # Позитивный тест: дедлайн в будущем
    mock_datetime.now.return_value = datetime(2025, 5, 10)
    mock_datetime.side_effect = lambda *a, **kw: datetime(*a, **kw)
    assert check_project_deadline(1) is True

@patch("task_manager.get_project_deadline", return_value=datetime(2025, 5, 15))
@patch("task_manager.datetime")
def test_check_project_deadline_negative(mock_datetime, mock_get_deadline):
    # Негативный тест: дедлайн прошел
    mock_datetime.now.return_value = datetime(2025, 5, 16)
    mock_datetime.side_effect = lambda *a, **kw: datetime(*a, **kw)
    assert check_project_deadline(1) is False

def test_check_project_deadline_negative_invalid_id():
    # Негативный тест: некорректный ID проекта
    with pytest.raises(ValueError, match="Invalid project ID."):
        check_project_deadline(0)

@patch("task_manager.get_project_deadline", return_value=datetime(2025, 5, 15))
@patch("task_manager.datetime")
def test_check_project_deadline_today(mock_datetime, mock_get_deadline):
    # Позитивный тест: дедлайн сегодня
    mock_datetime.now.return_value = datetime(2025, 5, 15)
    mock_datetime.side_effect = lambda *a, **kw: datetime(*a, **kw)
    assert check_project_deadline(1) is True

# ===== Тесты send_task_notification =====
@patch("task_manager.send_email", return_value=True)
def test_send_task_notification_positive(mock_send, valid_email, task_info):
    # Позитивный тест: успешная отправка уведомления
    assert send_task_notification(valid_email, task_info) is True

@patch("task_manager.send_email", return_value=True)
def test_send_task_notification_status_done(mock_send):
    # Позитивный тест: статус "завершена"
    assert send_task_notification("user@example.com", {"title": "Task X", "status": "done"}) is True

def test_send_task_notification_invalid_email(task_info):
    # Негативный тест: email некорректный
    with pytest.raises(ValueError, match="Invalid email."):
        send_task_notification("bad_email", task_info)

@patch("task_manager.send_email", return_value=False)
def test_send_task_notification_smtp_failure(mock_send):
    # Негативный тест: сбой отправки SMTP
    assert send_task_notification("user@example.com", {"title": "T"}) is False
