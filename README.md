# Техническое Задание

## Введение

### Цель проекта

Разработать онлайн-платформу, которая позволит пользователям обмениваться
книгами, создавая удобное и доступное пространство для обмена литературными
произведениями.
Описание проекта
Онлайн-платформа для обмена книгами позволит пользователям зарегистрироваться,
добавлять свои книги в личную библиотеку и искать книги других пользователей для
обмена. Каждая книга будет иметь описание, обложку и информацию о доступности
для обмена. Пользователи смогут просматривать доступные книги и отправлять
запросы на обмен.

### Требования

#### Функциональные требования:

1. Регистрация пользователя с использованием электронной почты и пароля.
   Реализация регистрации через Google можно осуществить по желанию
   участников.
   Регистрация необходима в двух этапах:

    - Базовая регистрация: Пользователь проходит регистрацию, заполняя
      обязательные поля, такие как имя, номер телефона, пароль.
    - Добавление информации о доступных книгах: После успешного
      завершения базовой регистрации пользователь переходит на второй этап,
      где он указывает информацию о доступных книгах для обмена.
      Пользователь может добавить книги, указывая их название, автора, жанр
      и другую релевантную информацию. Дополнительные детали: такие как
      состояние книги (новая, б/у и т. д.), описание или фотография могут быть
      добавлены для предоставления более подробной информации о книгах.
2. Возможность добавления книг в личную библиотеку с указанием автора,
   названия, описания и обложки (фото лицевой стороны книги).
3. Сложный поиск книг по автору, названию или жанру.
    - Поиск книг для обмена(Выдача в виде ленты):
      Пользователь может использовать поисковую функцию на платформе,
      чтобы найти книги, которые ему интересны для обмена.
      Пользователь может фильтровать результаты поиска по жанру, автору,
      языку и другим параметрам.
4. Отправка запросов на обмен книгами между пользователями.
   -  Пользователь выбирает книгу, которую он хотел бы получить в обмен на
   свою книгу. На странице книги есть кнопка или форма для отправки
   запроса на обмен. Пользователь нажимает на эту кнопку или заполняет
   форму, указывая детали своей книги и предлагая обмен. (В дальнейшем
   можно добавить возможность добавления книг в коллекцию и выборе
   книги из коллекции при отправке запроса на обмен).
   - Подтверждение запроса: Владелец выбранной книги получает
   уведомление о запросе на обмен. Он может просмотреть информацию о
   книге, предложенную в обмен, и принять или отклонить запрос.
   - Согласование деталей обмена: Если владелец выбранной книги
   принимает запрос, они имеют возможность связаться по номеру
   телефона, который указан в профиле, для согласования деталей обмена,
   таких как место и время встречи или адрес для отправки книги.
   - Обмен книгами: Пользователи встречаются лично в указанном месте и
   времени или организуют доставку книг по указанному адресу. Обмен
   происходит, когда каждый пользователь передает свою книгу другому
   участнику.
   - Подтверждение завершения обмена: После завершения обмена каждый
   пользователь подтверждает на платформе, что обмен состоялся успешно.
   Пользователи могут оставить оценку друг друга после завершения
   обмена с отзывом(поле необязательное).
5. Уведомления о новых запросах и статусе обмена книгами. Статусы:
   - Ожидание подтверждения: Этот статус указывает, что запрос на обмен
   был отправлен, но еще не получено подтверждение от владельца
   выбранной книги. Пользователь, отправивший запрос, ожидает ответа и
   решения владельца книги.
   - Запрос принят: Когда владелец выбранной книги принимает запрос,
   статус изменяется на "Запрос принят". Это означает, что оба участника
   согласны на обмен и готовы перейти к следующему шагу.
   - Детали обмена согласованы: После принятия запроса, пользователи
   согласовывают детали обмена, такие как место, время и способ передачи
   книг. Когда все детали обмена были согласованы, статус изменяется на
   "Детали обмена согласованы".
   - Обмен завершен: После того, как обмен книгами произошел успешно,
   статус изменяется на "Обмен завершен". Оба пользователей
   подтверждают, что книги были переданы и обмен прошел успешно.
   - Отклонен: Если владелец выбранной книги отклоняет запрос на обмен,
   статус изменяется на "Отклонен". Пользователь, отправивший запрос,
   уведомляется о том, что обмен не состоится.
   - Отменен: Если пользователь отменяет запрос на обмен до его
   подтверждения или в процессе согласования деталей, статус может быть
   изменен на "Отменен".
6. Возможность подтверждения или отклонения запросов на обмен.
7. Обновление статуса книги в библиотеке после успешного обмена.
8. Рейтинг пользователей на основе успешных обменов.Нефункциональные требования:
1. Платформа должна быть доступна через веб-интерфейс.
2. Дизайн пользовательского интерфейса должен быть интуитивно понятным и
   привлекательным.
3. Система должна быть масштабируемой и способной обрабатывать большое
   количество пользователей и книг.
4. Безопасность данных и конфиденциальность пользователей должны быть
   обеспечены.
   Технические детали
   Технологии:

- Язык программирования: Python
- Фреймворк веб-приложений: Django
- Фронтенд: HTML, CSS, JavaScript, ReactJS
- СУБД: PostgreSQL
- Хостинг: AWS или аналогичный провайдер
  Архитектура:
- Веб-сервер на базе фреймворка Django.
- Хранение данных о пользователях, книгах и запросах в СУБД PostgreSQL.
- Реализация API для взаимодействия между клиентом и сервером.
- Фронтенд с использованием HTML, CSS, JavaScript и ReactJS для создания
  пользовательского интерфейса.
  План работ
  Фазы разработки:
- Анализ требований и проектирование системы.
- Разработка базовой функциональности и интерфейса.
- Тестирование и отладка.
- Внедрение и запуск платформы.
- Мониторинг и поддержка.
  Распределение задач:
- Разработка серверной части и API - 2 недели.
- Разработка клиентской части и пользовательского интерфейса - 2 недели.
- Тестирование и отладка - 1 неделя.
- Внедрение и запуск - 1 неделя.
- Мониторинг и поддержка - постоянно после запуска. (В рамках подписанного
  меморандума)Ожидаемые результаты:
- Запущенная и работающая онлайн-платформа для обмена книгами.
- Разработанный и протестированный исходный код.
- Документация по установке, настройке и использованию платформы.
  Ограничения и допущения:
- В рамках данного проекта не требуется интеграция с платежными системами
  или доставкой книг.
- Платформа ориентирована на обмен книгами между физическими лицами, а не
  на коммерческую продажу.
- Поддержка нескольких языков и локализация не требуется в начальной версии
  проекта.