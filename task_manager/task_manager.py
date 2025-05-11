from datetime import datetime
from typing import Dict

# ===== Вспомогательные зависимости (мокируются в тестах) =====
def send_email(email: str, content: str) -> bool:
    """
    Отправка email-сообщения (эмулируется). В реальности — SMTP/почтовый сервис.
    """
    return True

def get_project_deadline(project_id: int) -> datetime:
    """
    Получение дедлайна проекта (эмулируется как внешний источник: БД/репозиторий).
    """
    return datetime(2025, 5, 15)

# ===== Бизнес-логика Task Manager =====
def create_task(project_id: int, title: str, deadline: datetime) -> int:
    """
    Создает задачу в рамках проекта. Возвращает ID задачи.
    """
    if not title:
        raise ValueError("Title cannot be empty.")
    if deadline < datetime.now():
        raise ValueError("Deadline cannot be in the past.")
    if project_id <= 0:
        raise ValueError("Invalid project ID.")
    return 42  # Эмуляция ID созданной задачи

def track_time(task_id: int, hours: float) -> float:
    """
    Добавляет отработанные часы к задаче. Возвращает обновленное значение.
    """
    if task_id <= 0:
        raise ValueError("Invalid task ID.")
    if hours <= 0:
        raise ValueError("Hours must be positive.")
    if hours > 1000:
        raise ValueError("Unrealistic number of hours.")
    return hours

def calculate_invoice(hours: float, rate: float, currency: str) -> float:
    """
    Рассчитывает счет по часам, ставке и валюте. Поддержка: USD, EUR.
    """
    if hours < 0 or rate < 0:
        raise ValueError("Hours and rate must be non-negative.")
    if currency not in ("USD", "EUR"):
        raise ValueError("Unsupported currency.")
    return round(hours * rate, 2)

def check_project_deadline(project_id: int) -> bool:
    """
    Проверяет, не истек ли срок проекта. Использует внешний источник даты.
    """
    if project_id <= 0:
        raise ValueError("Invalid project ID.")
    deadline = get_project_deadline(project_id)
    return datetime.now() <= deadline

def send_task_notification(email: str, task_info: Dict) -> bool:
    """
    Отправляет уведомление о задаче. Использует send_email().
    """
    if "@" not in email:
        raise ValueError("Invalid email.")
    content = f"Task '{task_info.get('title')}' has status: {task_info.get('status', 'unknown')}"
    return send_email(email, content)