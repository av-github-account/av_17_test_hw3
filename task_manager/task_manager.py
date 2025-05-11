from datetime import datetime
from typing import Dict


# Функция 1: Создание задачи
def create_task(project_id: int, title: str, deadline: datetime) -> int:
    """
    Создает задачу в рамках проекта и возвращает ID созданной задачи.
    Предполагается, что project_id валиден, заголовок не пустой и дедлайн в будущем.
    """
    if not title:
        raise ValueError("Title cannot be empty.")
    if deadline < datetime.now():
        raise ValueError("Deadline cannot be in the past.")
    if project_id <= 0:
        raise ValueError("Invalid project ID.")
    
    # Предположим, что задача сохраняется в базу и возвращается ID
    task_id = 42  # Мокаем возвращаемое значение
    return task_id


# Функция 2: Учет времени
def track_time(task_id: int, hours: float) -> float:
    """
    Добавляет отработанные часы к задаче. Возвращает новое общее количество часов.
    """
    if task_id <= 0:
        raise ValueError("Invalid task ID.")
    if hours <= 0:
        raise ValueError("Hours must be positive.")
    if hours > 1000:
        raise ValueError("Unrealistic number of hours.")
    
    # Предположим, что обновляется в БД
    return hours  # Возвращаем как будто бы общее количество часов стало равно hours


# Функция 3: Расчет счета
def calculate_invoice(hours: float, rate: float, currency: str) -> float:
    """
    Рассчитывает сумму счета на основе часов, ставки и валюты.
    Поддерживаемые валюты: USD, EUR.
    """
    if hours < 0 or rate < 0:
        raise ValueError("Hours and rate must be non-negative.")
    if currency not in ("USD", "EUR"):
        raise ValueError("Unsupported currency.")
    
    result = round(hours * rate, 2)
    return result


# Функция 4: Проверка дедлайна проекта
def check_project_deadline(project_id: int) -> bool:
    """
    Проверяет, истёк ли дедлайн проекта. Возвращает False, если срок прошёл.
    Мокается получение даты из базы.
    """
    if project_id <= 0:
        raise ValueError("Invalid project ID.")
    
    deadline = datetime(2025, 5, 15)  # Здесь бы подтягивалось из БД
    return datetime.now() <= deadline


# Функция 5: Отправка уведомлений
def send_task_notification(email: str, task_info: Dict) -> bool:
    """
    Отправляет уведомление на email с информацией о задаче.
    Мокается отправка письма.
    """
    if "@" not in email:
        raise ValueError("Invalid email.")
    
    # Предположим, что здесь вызывается внешний SMTP-сервис
    sent = True  # Мокаем успешную отправку
    return sent
