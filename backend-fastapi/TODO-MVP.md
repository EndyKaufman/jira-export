# TODO: Backend API JIRA Export - MVP версия

## Описание MVP
Backend MVP фокусируется на **базовом REST API** для просмотра задач без сложных enterprise функций как real-time, multi-tenancy или аналитика.

## Функции MVP
- Базовая API аутентификация JIRA (Basic Auth)
- REST endpoints для получения списков задач и детальной информации
- Простая фильтрация по статусу, приоритету, исполнителю
- Базовая PDF генерация для отдельных задач
- Простое кэширование без сложной инвалидации
- Полнотекстовый поиск по задачам
- Офлайн поддержка для клиентских приложений
- Базовая безопасность (CORS, валидация)

## Этапы разработки MVP

### Этап 1: Базовая архитектура (3-4 дня)
- [ ] **1.1 FastAPI проект setup** (1-2 дня)
  - Простая FastAPI структура
  - Basic requirements.txt
  - Environment configuration
  - Simple logging setup

- [ ] **1.2 Database setup** (1-2 дня)
  - SQLite для development (простота)
  - Simple SQLAlchemy models
  - Basic database schema
  - Connection management

### Этап 2: Core API структура (4-5 дней)
- [ ] **2.1 API routes structure** (2-3 дня)
  - Authentication endpoints
  - Tasks endpoints
  - Health check endpoints
  - Basic error handling

- [ ] **2.2 Request/Response models** (1-2 дня)
  - Pydantic models для validation
  - API schema definition
  - Error response models
  - Basic OpenAPI documentation

### Этап 3: JIRA integration (6-8 дней)
- [ ] **3.1 JIRA HTTP client** (3-4 дня)
  - Basic auth JIRA connection
  - HTTP client с requests
  - Basic error handling
  - Connection testing endpoint

- [ ] **3.2 JIRA API wrapper** (2-3 дня)
  - Issues retrieval
  - Project information
  - User information
  - Basic field mapping

- [ ] **3.3 API endpoints implementation** (1 день)
  - GET /auth/test-connection
  - GET /projects
  - GET /issues
  - GET /issues/{id}

### Этап 4: Authentication system (4-5 дней)
- [ ] **4.1 Simple auth система** (2-3 дня)
  - Store JIRA credentials securely
  - Basic session management
  - Simple API key для client apps
  - Credential validation

- [ ] **4.2 Authentication middleware** (1-2 дня)
  - Request authentication
  - Error handling для auth failures
  - Basic rate limiting

### Этап 5: Filtering и search (5-6 дней)
- [ ] **5.1 Basic filtering** (2-3 дня)
  - Query parameter parsing
  - Status filtering
  - Assignee filtering
  - Priority filtering

- [ ] **5.2 Search implementation** (2-3 дня)
  - Full-text search через JIRA API
  - Simple search endpoint
  - Search result formatting

- [ ] **5.3 Query optimization** (1 день)
  - Basic query caching
  - Parameter validation
  - Error handling

### Этап 6: Caching system (4-5 дней)
- [ ] **6.1 Simple caching** (2-3 дня)
  - Redis или in-memory cache
  - Basic cache keys strategy
  - TTL management
  - Cache invalidation

- [ ] **6.2 API caching integration** (1-2 дня)
  - Cache middleware
  - Cache headers
  - Cache bypass options

### Этап 7: PDF generation (6-8 дней)
- [ ] **7.1 PDF service** (3-4 дня)
  - Choose PDF library (ReportLab или WeasyPrint)
  - Basic task template
  - PDF generation endpoint
  - File handling

- [ ] **7.2 PDF API integration** (2-3 дня)
  - POST /export/pdf
  - Async PDF generation
  - File download endpoint
  - Error handling

- [ ] **7.3 File management** (1 день)
  - Temporary file cleanup
  - File storage strategy
  - Basic security для file access

### Этап 8: Data persistence (4-5 дней)
- [ ] **8.1 Data models** (2-3 дня)
  - SQLAlchemy models для caching
  - Task data persistence
  - User session storage
  - Basic relationships

- [ ] **8.2 Data synchronization** (1-2 дня)
  - Basic sync logic
  - Data freshness tracking
  - Simple conflict handling

### Этап 9: API security и validation (3-4 дня)
- [ ] **9.1 Basic security** (1-2 дня)
  - CORS configuration
  - Input validation
  - SQL injection prevention
  - Basic request sanitization

- [ ] **9.2 Error handling** (1-2 дня)
  - Comprehensive error responses
  - HTTP status codes
  - Error logging
  - Client-friendly error messages

### Этап 10: Testing и documentation (4-6 дней)
- [ ] **10.1 Basic testing** (2-3 дня)
  - API endpoint tests
  - JIRA integration tests (mocked)
  - Basic load testing
  - Error scenario testing

- [ ] **10.2 API documentation** (1-2 дня)
  - OpenAPI/Swagger setup
  - Endpoint documentation
  - Example requests/responses
  - Postman collection

- [ ] **10.3 Manual testing** (1 день)
  - End-to-end testing с real JIRA
  - Performance testing
  - Error scenario validation

### Этап 11: Deployment preparation (3-4 дня)
- [ ] **11.1 Production setup** (2-3 дня)
  - Environment configuration
  - Database migration to PostgreSQL
  - Production dependencies
  - Health checks

- [ ] **11.2 Docker containerization** (1 день)
  - Basic Dockerfile
  - Docker compose для development
  - Environment variables

## Общая оценка времени MVP

**Общее время разработки: 45-60 дней (9-12 недель)**

### Распределение времени:
- Базовая архитектура: 4 дня
- API структура: 5 дней
- JIRA integration: 8 дней
- Authentication: 5 дней
- Filtering и search: 6 дней
- Caching: 5 дней
- PDF generation: 8 дней
- Data persistence: 5 дней
- Security: 4 дней
- Testing: 6 дней
- Deployment: 4 дня

### Технические ограничения MVP:
- SQLite для development, PostgreSQL для production
- Basic auth только (без OAuth, JWT)
- Simple caching без сложной invalidation
- Single JIRA instance support
- Basic PDF templates
- No real-time updates
- No advanced analytics
- No webhook processing
- No API versioning

### Что НЕ входит в MVP:
- JWT authentication
- Real-time WebSocket connections
- Multi-tenancy support
- Advanced caching strategies
- Webhook processing
- Analytics и metrics
- API versioning
- Background task processing
- Advanced monitoring
- Load balancing preparation

## API Endpoints MVP

### Authentication
- `POST /auth/login` - Basic JIRA authentication
- `GET /auth/test` - Test JIRA connection
- `POST /auth/logout` - Clear session

### Projects и Issues
- `GET /projects` - List available projects
- `GET /projects/{id}/issues` - Get project issues
- `GET /issues` - Search issues с basic filtering
- `GET /issues/{id}` - Get issue details

### Search и Filtering
- `GET /search?q={query}` - Full-text search
- `GET /issues?status={status}&assignee={user}` - Basic filtering

### Export
- `POST /export/pdf` - Generate PDF для single issue
- `GET /export/{id}/download` - Download generated PDF

### Utility
- `GET /health` - Health check
- `GET /docs` - API documentation

## Технические требования MVP
- Python 3.9+
- FastAPI 0.95+
- SQLAlchemy 2.0+
- PostgreSQL для production
- Redis для caching (optional)
- ReportLab для PDF
- Requests для HTTP calls
- Pydantic для validation

## Performance targets MVP
- Response time: <500ms для most endpoints
- PDF generation: <5 seconds для single task
- Concurrent users: 10-50
- Database size: <1GB

## Критерии готовности MVP
- [ ] Successful connection к test JIRA instance
- [ ] Retrieve и display 1000+ issues
- [ ] Apply basic filters (status, assignee, priority)
- [ ] Generate readable PDF для single issue
- [ ] Basic caching working (faster subsequent requests)
- [ ] Full-text search returning relevant results
- [ ] API documentation accessible через /docs
- [ ] Error handling не ломает API
- [ ] Docker container running in production
- [ ] Basic load test (10 concurrent users)

**Результат MVP**: Функциональный REST API для базового взаимодействия с JIRA с поддержкой просмотра задач, фильтрации и PDF экспорта.