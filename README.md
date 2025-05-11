# av_17_test_hw3
# Инструкция по тестированию Task Manager и Booking Service

## Task Manager

### 1. create_task(project_id, title, deadline)

* test_create_task_positive – Позитивный. Проверяет успешное создание задачи с валидными project_id, title и дедлайном в будущем.
* test_create_task_negative_empty_title – Негативный. Проверяет, что пустой заголовок вызывает исключение.
* test_create_task_negative_past_deadline – Негативный. Проверяет, что дедлайн в прошлом вызывает исключение.
* test_create_task_negative_invalid_project – Негативный. Проверяет, что нулевой или отрицательный project_id вызывает исключение.

### 2. track_time(task_id, hours)

* test_track_time_positive – Позитивный. Проверяет добавление валидного количества часов к задаче.
* test_track_time_positive_minimal_hours – Позитивный. Проверяет добавление минимально возможного положительного значения (0.01).
* test_track_time_negative_zero_hours – Негативный. Проверяет, что 0 часов вызывает исключение.
* test_track_time_negative_negative_hours – Негативный. Проверяет, что отрицательное количество часов вызывает исключение.
* test_track_time_negative_too_many_hours – Негативный. Проверяет, что слишком большое число часов вызывает исключение.

### 3. calculate_invoice(hours, rate, currency)

* test_calculate_invoice_positive – Позитивный. Проверяет корректный расчет счета с разными параметрами.
* test_calculate_invoice_negative_unsupported_currency – Негативный. Проверяет, что неподдерживаемая валюта вызывает исключение.
* test_calculate_invoice_negative_negative_hours – Негативный. Проверяет, что отрицательные значения часов вызывают исключение.
* test_calculate_invoice_negative_zero_rate – Позитивный. Проверяет корректность расчета, если ставка равна нулю.

### 4. check_project_deadline(project_id)

* test_check_project_deadline_positive – Позитивный. Проверяет, что проект с дедлайном в будущем считается действующим.
* test_check_project_deadline_today – Позитивный. Проверяет, что проект с дедлайном сегодня считается действующим.
* test_check_project_deadline_negative – Негативный. Проверяет, что проект с просроченным дедлайном считается просроченным.
* test_check_project_deadline_negative_invalid_id – Негативный. Проверяет, что project_id <= 0 вызывает исключение.

### 5. send_task_notification(email, task_info)

* test_send_task_notification_positive – Позитивный. Проверяет успешную отправку уведомления при корректных данных.
* test_send_task_notification_status_done – Позитивный. Проверяет отправку уведомления для завершенной задачи.
* test_send_task_notification_invalid_email – Негативный. Проверяет, что невалидный email вызывает исключение.
* test_send_task_notification_smtp_failure – Негативный. Проверяет, что при сбое SMTP функция возвращает False.

## Booking Service

### 1. calc_price(base_price, discount, count)

* test_calc_price_positive – Позитивный. Проверяет корректный расчет стоимости билетов с учетом скидки.
* test_calc_price_negative_discount – Негативный. Проверяет, что отрицательная скидка вызывает исключение.
* test_calc_price_negative_too_big_discount – Негативный. Проверяет, что скидка более 100% вызывает исключение.
* test_calc_price_negative_count – Негативный. Проверяет, что отрицательное количество билетов вызывает исключение.

### 2. check_availability(event_id, seats_requested)

* test_check_availability_positive_enough – Позитивный. Проверяет, что при достаточном количестве мест функция возвращает True.
* test_check_availability_positive_exact – Позитивный. Проверяет, что при точном совпадении количества мест возвращается True.
* test_check_availability_negative_insufficient – Негативный. Проверяет, что при нехватке мест возвращается False.
* test_check_availability_negative_invalid_request – Негативный. Проверяет, что запрос нуля или отрицательного количества мест вызывает исключение.

### 3. apply_promo_code(order_id, promo_code)

* test_apply_promo_code_positive_valid – Позитивный. Проверяет применение валидного и неиспользованного промокода.
* test_apply_promo_code_positive_another_valid – Позитивный. Проверяет применение другого корректного промокода.
* test_apply_promo_code_negative_used – Негативный. Проверяет, что использованный промокод не применяется.
* test_apply_promo_code_negative_empty – Негативный. Проверяет, что пустой промокод вызывает исключение.

### 4. generate_booking_ref(user_id, event_id)

* test_generate_booking_ref_positive_format – Позитивный. Проверяет корректность формата сгенерированного кода бронирования.
* test_generate_booking_ref_positive_unique – Позитивный. Проверяет, что коды бронирования при повторных вызовах уникальны.
* test_generate_booking_ref_negative_user – Негативный. Проверяет, что user_id <= 0 вызывает исключение.
* test_generate_booking_ref_negative_event – Негативный. Проверяет, что event_id <= 0 вызывает исключение.

### 5. send_notification_email(email, booking_details)

* test_send_notification_email_positive – Позитивный. Проверяет успешную отправку уведомления на корректный email.
* test_send_notification_email_positive_other – Позитивный. Проверяет успешную отправку с другими корректными параметрами.
* test_send_notification_email_negative_email – Негативный. Проверяет, что некорректный email вызывает исключение.
* test_send_notification_email_negative_smtp – Негативный. Проверяет, что при сбое почтового сервиса функция возвращает False.
