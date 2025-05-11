# test_task_manager.py

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

# -------------------------------
# Фикстуры
# -------------------------------

@pytest.fixture
def future_deadline():
    return datetime.now() + timedelta(days=5)

@pytest.fixture
def past_deadline():
    return datetime.now() - timedelta(days=1)

@pytest.fixture
def valid_email():
    return "user@example.com"

@pytest.fixture
def task_info():
    return {"title": "Task A", "status": "created"}


# -------------------------------
# Тесты для create_task
# -------------------------------

@pytest.mark.parametrize("project_id, title", [(1, "Task 1"), (99, "Important Task")])
def test_create_task_positive(project_id, title, future_deadline):
    # Позитивный тест: создаем задачу с валидными параметрами
    result = create_task(project_id, title, future_deadline)
    assert isinstance(result, int)

@pytest.mark.parametrize("title", ["", None])
def test_create_task_negative_empty_title(title, future_deadline):
    # Негативный тест: заголовок задачи пустой
    with pytest.raises(ValueError, match="Title cannot be empty."):
        create_task(1, title, future_deadline)

def test_create_task_negative_past_deadline():
    # Негативный тест: дедлайн в прошлом
    with pytest.raises(ValueError, match="Deadline cannot be in the past."):
        create_task(1, "Task X", datetime.now() - timedelta(days=2))

def test_create_task_negative_invalid_project():
    # Негативный тест: некорректный project_id
    with pytest.raises(ValueError, match="Invalid project ID."):
        create_task(0, "Valid title", datetime.now() + timedelta(days=2))


# -------------------------------
# Тесты для track_time
# -------------------------------

@pytest.mark.parametrize("task_id, hours", [(1, 5.0), (10, 2.5)])
def test_track_time_positive(task_id, hours):
    # Позитивный тест: добавление валидных часов
    result = track_time(task_id, hours)
    assert result == hours

def test_track_time_negative_zero_hours():
    # Негативный тест: 0 часов
    with pytest.raises(ValueError, match="Hours must be positive."):
        track_time(1, 0)

def test_track_time_negative_negative_hours():
    # Негативный тест: отрицательное значение часов
    with pytest.raises(ValueError, match="Hours must be positive."):
        track_time(1, -3)

def test_track_time_negative_unrealistic_hours():
    # Негативный тест: слишком большое количество часов
    with pytest.raises(ValueError, match="Unrealistic number of hours."):
        track_time(1, 10000)


# -------------------------------
# Тесты для calculate_invoice
# -------------------------------

@pytest.mark.parametrize("hours, rate, currency, expected", [(10, 50, "USD", 500.0), (2.5, 100, "EUR", 250.0)])
def test_calculate_invoice_positive(hours, rate, currency, expected):
    # Позитивный тест: расчет счета с валидными параметрами
    result = calculate_invoice(hours, rate, currency)
    assert result == expected

def test_calculate_invoice_negative_unsupported_currency():
    # Негативный тест: неподдерживаемая валюта
    with pytest.raises(ValueError, match="Unsupported currency."):
        calculate_invoice(5, 10, "JPY")

def test_calculate_invoice_negative_negative_hours():
    # Негативный тест: отрицательное количество часов
    with pytest.raises(ValueError, match="Hours and rate must be non-negative."):
        calculate_invoice(-1, 10, "USD")

def test_calculate_invoice_negative_zero_rate():
    # Позитивный тест: ставка 0
    result = calculate_invoice(10, 0, "USD")
    assert result == 0.0


# -------------------------------
# Тесты для check_project_deadline
# -------------------------------

@patch("task_manager.datetime")
def test_check_project_deadline_positive(mock_datetime):
    # Позитивный тест: дедлайн в будущем
    mock_datetime.now.return_value = datetime(2025, 5, 10)
    mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
    assert check_project_deadline(1) is True

@patch("task_manager.datetime")
def test_check_project_deadline_negative_past(mock_datetime):
    # Негативный тест: дедлайн в прошлом
    mock_datetime.now.return_value = datetime(2025, 5, 20)
    mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
    assert check_project_deadline(1) is False

def test_check_project_deadline_negative_invalid_project():
    # Негативный тест: неверный project_id
    with pytest.raises(ValueError, match="Invalid project ID."):
        check_project_deadline(-2)

@patch("task_manager.datetime")
def test_check_project_deadline_today(mock_datetime):
    # Позитивный тест: дедлайн сегодня
    mock_datetime.now.return_value = datetime(2025, 5, 15)
    mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
    assert check_project_deadline(1) is True


# -------------------------------
# Тесты для send_task_notification
# -------------------------------

@patch("task_manager.send_task_notification", return_value=True)
def test_send_task_notification_positive(mock_send, valid_email, task_info):
    # Позитивный тест: успешная отправка уведомления
    result = send_task_notification(valid_email, task_info)
    assert result is True

def test_send_task_notification_negative_invalid_email(task_info):
    # Негативный тест: некорректный email
    with pytest.raises(ValueError, match="Invalid email."):
        send_task_notification("bad_email", task_info)

@patch("task_manager.send_task_notification", return_value=False)
def test_send_task_notification_negative_smtp_error(mock_send):
    # Негативный тест: сбой при отправке почты (мокаем False)
    result = send_task_notification("user@example.com", {"title": "A"})
    assert result is False

@patch("task_manager.send_task_notification", return_value=True)
def test_send_task_notification_positive_status_done(mock_send):
    # Позитивный тест: отправка уведомления о завершенной задаче
    result = send_task_notification("user@example.com", {"title": "X", "status": "done"})
    assert result is True
