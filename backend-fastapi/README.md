# Backend API для JIRA Export

## Описание
REST API backend сервер для работы с JIRA, предоставляющий полнофункциональный программный интерфейс для получения списка задач, применения различных фильтров и экспорта задач в PDF формат. Сервер служит промежуточным слоем между клиентскими приложениями и JIRA API, обеспечивая кэширование, авторизацию и дополнительную бизнес-логику. Поддерживает многопользовательский режим работы с подключением к множественным JIRA инстансам и real-time уведомления об изменениях.

## Функции MVP (первая версия)
- **API аутентификации JIRA**: Базовое управление подключениями к JIRA серверам через Basic Auth
- **Управление задачами**: REST endpoints для получения списков задач и детальной информации
- **Базовая фильтрация**: API для простых фильтров по статусу, приоритету, исполнителю
- **PDF генерация**: Базовая генерация PDF отчетов для отдельных задач
- **Простое кэширование**: Основное кэширование данных JIRA без сложной инвалидации
- **Поиск**: Полнотекстовый поиск по задачам
- **Детальная информация**: API для получения полной информации о задачах с комментариями
- **Офлайн поддержка**: Базовая синхронизация данных для офлайн режима
- **Базовая безопасность**: CORS, базовая валидация запросов

## Основные функции (полная версия)
- **Продвинутая аутентификация**: Множественные методы (Token, OAuth) с JWT авторизацией
- **JQL конструктор**: Полнофункциональная JQL поддержка с валидацией
- **Real-time уведомления**: WebSocket соединения для мгновенных уведомлений
- **Multi-tenancy**: Поддержка множественных JIRA инстансов и пользователей
- **Пакетные операции**: Массовые операции с задачами, групповой экспорт
- **Аналитика и метрики**: Сбор статистики использования и производительности
- **Webhook обработка**: Обработка JIRA webhook для real-time обновлений
- **API версионирование**: Поддержка множественных версий API с backward compatibility
- **Управление файлами**: Полное управление вложениями с безопасностью
- **Продвинутые отчеты**: Настраиваемые шаблоны и асинхронная обработказоляцией данных и конфигураций
- **Поиск и автодополнение**: Полнотекстовый поиск по задачам с автодополнением для JQL запросов и историей поисков
- **Быстрые фильтры**: Предустановленные фильтры по статусу, приоритету, исполнителю, датам с возможностью создания пользовательских наборов
- **Детальная информация о задачах**: API для получения полной информации включая комментарии, вложения, историю изменений с рендерингом JIRA разметки
- **Пакетные операции**: Массовые операции с задачами, групповой экспорт в PDF, пакетное применение фильтров
- **Офлайн поддержка**: Синхронизация данных для офлайн режима клиентских приложений с конфликт-резолюшеном
- **Аналитика и метрики**: Сбор статистики использования, производительности запросов, популярности фильтров
- **Webhook обработка**: Обработка JIRA webhook событий для real-time обновления кэшированных данных
- **Файловое управление**: Безопасное управление вложениями задач, временными файлами с контролем доступа
- **API версионирование**: Поддержка множественных версий API с backward compatibility и миграционными путями

## Технические возможности
- **Асинхронная архитектура**: FastAPI с полной поддержкой async/await для высокой производительности и масштабируемости
- **Database ORM**: SQLAlchemy 2.0+ с алхимией миграций, connection pooling и query optimization
- **Кэширование производительности**: Redis для высокоскоростного кэширования с поддержкой кластеризации и персистентности
- **Background задачи**: Celery/RQ для асинхронной обработки длительных операций (PDF генерация, синхронизация данных)
- **JWT авторизация**: Современная система авторизации с refresh токенами, scope-based permissions и session management
- **WebSocket поддержка**: Real-time двусторонняя коммуникация с управлением соединениями и broadcasting
- **API Security**: Comprehensive security с rate limiting, CORS, request validation, security headers и audit logging
- **Мониторинг и наблюдаемость**: Prometheus метрики, structured logging, health checks, performance monitoring
- **Контейнеризация**: Docker support с multi-stage builds, security scanning и orchestration готовность
- **CI/CD интеграция**: Automated testing, security scanning, deployment pipeline с Infrastructure as Code
- **Горизонтальное масштабирование**: Load balancer готовность, database read replicas, stateless architecture
- **Data persistence**: PostgreSQL с полнотекстовым поиском, индексированием, партиционированием для больших объемов данных
- **HTTP оптимизация**: Response compression, query complexity limits, connection pooling, retry mechanisms
- **Error handling**: Comprehensive error tracking с Sentry интеграцией, graceful degradation, circuit breakers

## Технологии
- FastAPI 0.104+ (современный асинхронный веб-фреймворк с автогенерацией OpenAPI документации)
- SQLAlchemy 2.0+ (мощный ORM с поддержкой async операций и advanced query capabilities) 
- PostgreSQL 14+ (основная реляционная база данных с JSON поддержкой и full-text search)
- Redis 6+ (высокоскоростное кэширование, session хранилище и message broker для real-time функций)
- Celery/RQ (distributed task queue для background обработки и асинхронных операций)
- JWT (JSON Web Tokens для stateless аутентификации с refresh token поддержкой)
- WebSocket (real-time двусторонняя коммуникация для live updates и notifications)
- Docker (контейнеризация с multi-stage builds для production deployment)
- Pydantic (мощная валидация данных и serialization с automatic API documentation)
- Alembic (database миграции с версионированием и rollback capabilities)
- Requests/HTTPX (HTTP клиенты для JIRA API интеграции с retry logic и connection pooling)
- WeasyPrint/ReportLab (PDF генерация библиотеки с rich formatting и template support)
- Prometheus (метрики и мониторинг производительности с Grafana integration)
- Pytest (comprehensive testing framework с fixtures, mocking и coverage reporting)
- Uvicorn/Gunicorn (ASGI серверы для production deployment с worker management)
- Nginx (reverse proxy, load balancing, SSL termination для production environments)

## Статус разработки
🚧 **В РАЗРАБОТКЕ** - Реализован полнофункциональный REST API для работы с JIRA.

Полный функционал описан в планах разработки [TODO-MVP.md](TODO-MVP.md) и [TODO-FULL.md](TODO-FULL.md) с детализированным планом разработки, включающим 11 основных этапов MVP (45-60 дней) и 15 этапов полной версии (115-160 дней) с временными оценками.

## Текущая функциональность
API обеспечивает полноценную работу с JIRA:
- **Аутентификация**: `/auth/login` - подключение к JIRA серверам
- **Управление задачами**: `/tasks` - получение списков задач с пагинацией
- **Фильтрация**: `/tasks/filter` - по статусу, приоритету, исполнителю
- **Выбор задач**: `/tasks/selection` - управление выбором задач
- **Действия**: `/tasks/{task_id}/action` - детали, PDF, JIRA ссылки
- **Массовые операции**: `/tasks/bulk/*` - массовый экспорт, очистка выбора
- **PDF экспорт**: `/tasks/{task_id}/export-pdf` - генерация PDF отчетов
- **Статистика**: `/status/tasks` - аналитика по задачам

## Технологии
- FastAPI 0.104+ (современный асинхронный веб-фреймворк с автогенерацией OpenAPI документации)
- SQLAlchemy 2.0+ (мощный ORM с поддержкой async операций) 
- PostgreSQL 14+ (основная реляционная база данных с JSON поддержкой)
- Redis 6+ (высокоскоростное кэширование и message broker)
- Celery/RQ (distributed task queue для background обработки)
- Pydantic (мощная валидация данных и serialization)
- Uvicorn/Gunicorn (ASGI серверы для production deployment)

## Установка и запуск

### Установка зависимостей
```bash
cd backend-fastapi
pip install -r requirements.txt
```

### Запуск сервера для разработки
```bash
# Запуск через основной файл
python main.py

# Или запуск через uvicorn напрямую
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Доступные эндпоинты

После запуска сервер будет доступен по адресу: `http://localhost:8000`

#### Основные API эндпоинты:
- `GET /` - Корневой эндпоинт с информацией об API
- `POST /auth/login` - Аутентификация в JIRA
- `GET /tasks` - Получение списка задач с пагинацией
- `POST /tasks/filter` - Фильтрация задач по критериям
- `GET /tasks/{task_id}` - Получение деталей конкретной задачи
- `POST /tasks/{task_id}/export-pdf` - Экспорт задачи в PDF
- `POST /tasks/selection` - Управление выбором задач
- `GET /tasks/selected` - Получение списка выбранных задач
- `POST /tasks/bulk/export-pdf` - Массовый экспорт в PDF
- `POST /tasks/bulk/toggle-all` - Переключение выбора всех задач
- `GET /health` - Проверка состояния API
- `GET /status/tasks` - Статистика по задачам

#### Документация API:
- `GET /docs` - Автоматическая документация Swagger UI
- `GET /redoc` - Альтернативная документация ReDoc

### Примеры запросов

```bash
# Получение списка задач
curl http://localhost:8000/tasks

# Фильтрация задач по статусу
curl -X POST http://localhost:8000/tasks/filter \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress", "page": 1, "per_page": 10}'

# Экспорт задачи в PDF
curl -X POST http://localhost:8000/tasks/PROJ-123/export-pdf

# Массовый экспорт в PDF
curl -X POST http://localhost:8000/tasks/bulk/export-pdf \
  -H "Content-Type: application/json" \
  -d '{"task_ids": ["PROJ-123", "PROJ-124"], "action_type": "pdf_export"}'
```

## Структура проекта
- `main.py` - основной файл приложения
- `requirements.txt` - зависимости проекта
- `README.md` - документация проекта