# JIRA Export Mobile - Ionic Framework

Мобильное приложение для просмотра задач JIRA, фильтрации и экспорта в PDF на базе Ionic Framework с JavaScript.

## Технологии

### Основной стек
- **Ionic Framework 7.5+** - UI компоненты и навигация
- **Capacitor 5.5+** - нативная функциональность и мост к web-коду
- **Vanilla JavaScript (ES6+)** - бизнес-логика приложения
- **HTML5/CSS3** - разметка и стили
- **JIRA REST API v2** - интеграция с JIRA

### Нативные возможности
- **@capacitor/app** - управление жизненным циклом приложения
- **@capacitor/status-bar** - настройка статус-бара
- **@capacitor/keyboard** - работа с виртуальной клавиатурой
- **@capacitor/haptics** - тактильная обратная связь

### Платформы
- **Web (PWA)** - прогрессивное веб-приложение
- **Android** - нативное Android приложение (.apk/.aab)
- **iOS** - нативное iOS приложение (.ipa)
- **Desktop (Electron)** - десктопное приложение (опционально)

## Возможности

### 🔐 Авторизация
- Авторизация в JIRA через API Token
- Сохранение данных авторизации локально
- Проверка подключения к JIRA

### 🔍 Фильтрация задач
- Фильтрация по проекту
- Фильтрация по статусу (множественный выбор)
- Фильтрация по типу задачи (множественный выбор)
- Фильтрация по исполнителю
- Сохранение настроек фильтров

### 📋 Просмотр задач
- Список задач с подробной информацией
- Выбор задач с помощью чекбоксов
- Пагинация и infinite scroll
- Pull-to-refresh для обновления
- Отображение приоритета и статуса

### 📄 Действия с задачами
- Экспорт выбранных задач в PDF
- Открытие задач в веб-интерфейсе JIRA
- Выбор/снятие выбора всех задач
- Счетчик выбранных задач

## Структура проекта

```
mobile-ionic/
├── capacitor.config.json      # Конфигурация Capacitor
├── package.json              # Зависимости и скрипты
└── src/                      # Исходный код
    ├── index.html           # Главный HTML файл
    ├── css/
    │   └── styles.css       # Пользовательские стили
    └── js/
        └── app.js           # Основная логика приложения
```

## Установка и запуск

### Предварительные требования

1. Node.js 16+ и npm
2. Ionic CLI:
```bash
npm install -g @ionic/cli
```

3. Capacitor CLI:
```bash
npm install -g @capacitor/cli
```

#### Java Development Kit (JDK)
**ВАЖНО**: Для сборки Android приложений требуется совместимая версия JDK:
- **Скачать JDK**: https://adoptium.net/temurin/releases/
- **Рекомендуемая версия**: JDK 17 или JDK 21
- **После установки**: Настройте переменную окружения `JAVA_HOME`
- **Проверка**: Выполните `java -version` для проверки установки

#### Android Studio и Android SDK
**ВАЖНО**: Для разработки Android приложений требуется Android Studio:
- **Скачать Android Studio**: https://developer.android.com/studio
- **Что входит**: Android Studio включает Android SDK, эмуляторы и все необходимые инструменты
- **После установки**:
  - Настройте переменную окружения `ANDROID_HOME` на папку Android SDK
  - Установите Android SDK Build-tools (версия 30-34)
  - Создайте или настройте Android Virtual Device (AVD) для тестирования
  - Убедитесь, что Android SDK Platform Tools добавлены в PATH

### Установка зависимостей

```bash
cd mobile-ionic
npm install
```

### Разработка

```bash
# Запуск в браузере
npm run serve
# или
ionic serve

# Сборка проекта
npm run build
# или
ionic build
```

### Сборка для мобильных платформ

```bash
# Добавить платформу Android
ionic cap add android

# Добавить платформу iOS
ionic cap add ios

# Сборка и синхронизация
ionic cap build android
ionic cap build ios

# Открыть в IDE
ionic cap open android
ionic cap open ios
```

## Конфигурация

### JIRA API
Для работы с JIRA необходимо:

1. Создать API Token в настройках аккаунта JIRA
2. Указать URL вашего JIRA instance
3. Ввести email и API Token в приложении

### Backend интеграция
Приложение ожидает наличие backend API для экспорта PDF по адресу `/api/export/pdf`

## Основные компоненты

### JiraExportApp класс
Основной класс приложения, который управляет:
- Авторизацией в JIRA
- Загрузкой и фильтрацией задач
- Взаимодействием с UI компонентами
- Экспортом данных

### UI компоненты
- `ion-tabs` - навигация по вкладкам
- `ion-card` - карточки для группировки контента
- `ion-list` - список задач
- `ion-checkbox` - выбор задач
- `ion-infinite-scroll` - подгрузка данных

## Особенности реализации

### Миграция с NativeScript
Приложение было мигрировано с NativeScript на Ionic Framework:
- Сохранена вся функциональность
- Улучшена производительность
- Добавлена поддержка веб-платформы
- Упрощена разработка и деплой

### Адаптивный дизайн
- Автоматическое масштабирование для разных экранов
- Оптимизация для мобильных устройств
- Поддержка темной и светлой тем

### Оффлайн возможности
- Кэширование данных авторизации
- Сохранение настроек фильтров
- Graceful handling сетевых ошибок

## API интеграция

### JIRA REST API
Используемые эндпоинты:
- `/rest/api/2/myself` - проверка авторизации
- `/rest/api/2/search` - поиск задач

### Backend API
- `POST /api/export/pdf` - экспорт задач в PDF

## Безопасность

- API Token хранится локально
- HTTPS соединения для всех запросов
- Базовая авторизация для JIRA API
- Валидация входных данных

## Развертывание

### Веб-версия
Приложение может быть развернуто как PWA на любом веб-сервере.

### Мобильные приложения
Сборка нативных приложений через Capacitor для:
- Android (Google Play Store)
- iOS (Apple App Store)

## Troubleshooting

### Типичные проблемы

#### Ошибки сборки Android
**Проблема**: `Unsupported class file major version`
**Решение**: 
- Убедитесь, что используется совместимая версия JDK (17 или 21)
- Обновите Gradle до последней версии
- Очистите кэш: `./gradlew clean`

**Проблема**: `ANDROID_HOME not set`
**Решение**:
```bash
# Windows
set ANDROID_HOME=C:\Users\YourUser\AppData\Local\Android\Sdk
set PATH=%PATH%;%ANDROID_HOME%\platform-tools

# macOS/Linux
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

#### Проблемы с JIRA API
**Проблема**: `CORS errors` при тестировании в браузере
**Решение**: Используйте proxy сервер или тестируйте на реальном устройстве

**Проблема**: `401 Unauthorized`
**Решение**: 
- Проверьте правильность API Token
- Убедитесь, что email указан корректно
- Проверьте URL JIRA instance

### Лучшие практики

#### Разработка
- Используйте `ionic serve` для быстрой разработки в браузере
- Тестируйте на реальных устройствах для проверки нативной функциональности
- Регулярно синхронизируйте изменения: `npx cap sync`

#### Производительность
- Оптимизируйте размер изображений и ресурсов
- Используйте lazy loading для больших списков
- Минимизируйте количество DOM элементов

#### Безопасность
- Никогда не храните пароли в plain text
- Используйте HTTPS для всех API запросов
- Валидируйте все пользовательские вводы

## Дополнительные ресурсы

### Документация
- [Ionic Framework Documentation](https://ionicframework.com/docs)
- [Capacitor Documentation](https://capacitorjs.com/docs)
- [JIRA REST API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v2/)

### Полезные команды
```bash
# Проверка состояния Capacitor
npx cap doctor

# Просмотр логов устройства
npx cap run android --livereload

# Обновление Capacitor плагинов
npm update @capacitor/core @capacitor/cli

# Очистка проекта
npx cap clean android
rm -rf node_modules && npm install
```

## Поддержка

Для вопросов и предложений создавайте issues в репозитории проекта.

## Лицензия

MIT License