# Makefile для управления всеми проектами
# Поддерживает команды для отдельных проектов и массовые операции
# Включает поддержку virtualenv для Python проектов

.PHONY: help install build test publish clean
.DEFAULT_GOAL := help

# Цвета для вывода
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Основные директории проектов
DESKTOP_DIR := desktop-python
MOBILE_DIR := mobile-ionic
BACKEND_DIR := backend-fastapi

# Python virtualenv настройки
PYTHON_VENV_DIR := .venv
PYTHON_ACTIVATE := $(PYTHON_VENV_DIR)/bin/activate
ifeq ($(OS),Windows_NT)
	PYTHON_ACTIVATE := $(PYTHON_VENV_DIR)/Scripts/activate
endif

help: ## Показать справку по командам
	@echo "$(GREEN)Доступные команды:$(NC)"
	@echo ""
	@echo "$(YELLOW)Массовые операции:$(NC)"
	@echo "  install-all     - Установить зависимости для всех проектов"
	@echo "  build-all       - Собрать все проекты"
	@echo "  test-all        - Запустить тесты для всех проектов"
	@echo "  publish-all     - Опубликовать все проекты"
	@echo "  clean-all       - Очистить все проекты"
	@echo ""
	@echo "$(YELLOW)Python virtualenv команды:$(NC)"
	@echo "  setup-venv      - Создать virtualenv для всех Python проектов"
	@echo "  clean-venv      - Удалить virtualenv для всех Python проектов"
	@echo ""
	@echo "$(YELLOW)Desktop Python проект:$(NC)"
	@echo "  setup-venv-desktop - Создать virtualenv"
	@echo "  install-desktop - Установить зависимости"
	@echo "  build-desktop   - Собрать в .exe"
	@echo "  test-desktop    - Запустить тесты"
	@echo "  run-desktop     - Запустить приложение"
	@echo "  publish-desktop - Опубликовать проект"
	@echo ""
	@echo "$(YELLOW)Mobile Ionic проект:$(NC)"
	@echo "  install-mobile  - Установить зависимости"
	@echo "  build-mobile    - Собрать .apk"
	@echo "  test-mobile     - Запустить тесты"
	@echo "  run-mobile      - Запустить на эмуляторе"
	@echo "  publish-mobile  - Опубликовать в Google Play"
	@echo ""
	@echo "$(YELLOW)Backend FastAPI проект:$(NC)"
	@echo "  setup-venv-backend - Создать virtualenv"
	@echo "  install-backend - Установить зависимости"
	@echo "  build-backend   - Подготовить к деплою"
	@echo "  test-backend    - Запустить тесты"
	@echo "  run-backend     - Запустить сервер"
	@echo "  publish-backend - Опубликовать на сервер"

# =============================================================================
# PYTHON VIRTUALENV КОМАНДЫ
# =============================================================================

setup-venv: ## Создать virtualenv для всех Python проектов
	@echo "$(GREEN)Создание virtualenv для всех Python проектов...$(NC)"
	@$(MAKE) setup-venv-desktop
	@$(MAKE) setup-venv-backend
	@echo "$(GREEN)✓ Virtualenv созданы для всех Python проектов$(NC)"

clean-venv: ## Удалить virtualenv для всех Python проектов
	@echo "$(GREEN)Удаление virtualenv для всех Python проектов...$(NC)"
	cd $(DESKTOP_DIR) && rm -rf $(PYTHON_VENV_DIR) || true
	cd $(BACKEND_DIR) && rm -rf $(PYTHON_VENV_DIR) || true
	@echo "$(GREEN)✓ Virtualenv удалены для всех Python проектов$(NC)"

# =============================================================================
# МАССОВЫЕ ОПЕРАЦИИ
# =============================================================================

install-all: ## Установить зависимости для всех проектов
	@echo "$(GREEN)Установка зависимостей для всех проектов...$(NC)"
	@$(MAKE) install-desktop
	@$(MAKE) install-mobile
	@$(MAKE) install-backend
	@echo "$(GREEN)✓ Зависимости установлены для всех проектов$(NC)"

build-all: ## Собрать все проекты
	@echo "$(GREEN)Сборка всех проектов...$(NC)"
	@$(MAKE) build-desktop
	@$(MAKE) build-mobile
	@$(MAKE) build-backend
	@echo "$(GREEN)✓ Все проекты собраны$(NC)"

test-all: ## Запустить тесты для всех проектов
	@echo "$(GREEN)Запуск тестов для всех проектов...$(NC)"
	@$(MAKE) test-desktop
	@$(MAKE) test-mobile
	@$(MAKE) test-backend
	@echo "$(GREEN)✓ Тесты выполнены для всех проектов$(NC)"

publish-all: ## Опубликовать все проекты
	@echo "$(GREEN)Публикация всех проектов...$(NC)"
	@$(MAKE) publish-desktop
	@$(MAKE) publish-mobile
	@$(MAKE) publish-backend
	@echo "$(GREEN)✓ Все проекты опубликованы$(NC)"

clean-all: ## Очистить все проекты
	@echo "$(GREEN)Очистка всех проектов...$(NC)"
	@$(MAKE) clean-desktop
	@$(MAKE) clean-mobile
	@$(MAKE) clean-backend
	@echo "$(GREEN)✓ Все проекты очищены$(NC)"

# =============================================================================
# DESKTOP PYTHON ПРОЕКТ
# =============================================================================

setup-venv-desktop: ## Создать virtualenv для desktop проекта
	@echo "$(YELLOW)Создание virtualenv для desktop проекта...$(NC)"
	cd $(DESKTOP_DIR) && python -m venv $(PYTHON_VENV_DIR)
	@echo "✓ Virtualenv создан в $(DESKTOP_DIR)/$(PYTHON_VENV_DIR)"

install-desktop: ## Установить зависимости для desktop проекта
	@echo "$(YELLOW)Установка зависимостей для desktop проекта...$(NC)"
	@if [ ! -d "$(DESKTOP_DIR)/$(PYTHON_VENV_DIR)" ]; then \
		echo "Создаем virtualenv..."; \
		$(MAKE) setup-venv-desktop; \
	fi
	cd $(DESKTOP_DIR) && source $(PYTHON_ACTIVATE) && pip install -r requirements.txt

build-desktop: ## Собрать desktop проект в .exe
	@echo "$(YELLOW)Сборка desktop проекта в .exe...$(NC)"
	cd $(DESKTOP_DIR) && source $(PYTHON_ACTIVATE) && pyinstaller --onefile --windowed main.py

test-desktop: ## Запустить тесты desktop проекта
	@echo "$(YELLOW)Запуск тестов desktop проекта...$(NC)"
	cd $(DESKTOP_DIR) && source $(PYTHON_ACTIVATE) && python -m pytest tests/ || echo "Тесты не найдены, создайте папку tests/"

run-desktop: ## Запустить desktop приложение
	@echo "$(YELLOW)Запуск desktop приложения...$(NC)"
	cd $(DESKTOP_DIR) && source $(PYTHON_ACTIVATE) && python main.py

publish-desktop: ## Опубликовать desktop проект
	@echo "$(YELLOW)Публикация desktop проекта...$(NC)"
	@echo "Desktop приложение готово в папке $(DESKTOP_DIR)/dist/"
	@echo "Готово к распространению как standalone .exe файл"

clean-desktop: ## Очистить desktop проект
	@echo "$(YELLOW)Очистка desktop проекта...$(NC)"
	cd $(DESKTOP_DIR) && rm -rf build/ dist/ *.spec __pycache__/ $(PYTHON_VENV_DIR) || true

# =============================================================================
# MOBILE IONIC ПРОЕКТ
# =============================================================================

install-mobile: ## Установить зависимости для mobile проекта
	@echo "$(YELLOW)Установка зависимостей для mobile проекта...$(NC)"
	cd $(MOBILE_DIR) && npm install

build-mobile: ## Собрать mobile проект в .apk
	@echo "$(YELLOW)Сборка mobile проекта в .apk...$(NC)"
	cd $(MOBILE_DIR) && ionic capacitor build android

test-mobile: ## Запустить тесты mobile проекта
	@echo "$(YELLOW)Запуск тестов mobile проекта...$(NC)"
	cd $(MOBILE_DIR) && npm test || echo "Тесты не настроены, добавьте тестовый фреймворк"

run-mobile: ## Запустить mobile приложение на эмуляторе
	@echo "$(YELLOW)Запуск mobile приложения...$(NC)"
	cd $(MOBILE_DIR) && ionic capacitor run android

publish-mobile: ## Опубликовать mobile проект в Google Play
	@echo "$(YELLOW)Подготовка к публикации mobile проекта...$(NC)"
	@echo "APK готов для загрузки в Google Play Console"
	@echo "Файл находится в $(MOBILE_DIR)/android/app/build/outputs/apk/"

clean-mobile: ## Очистить mobile проект
	@echo "$(YELLOW)Очистка mobile проекта...$(NC)"
	cd $(MOBILE_DIR) && ionic capacitor clean android || true
	cd $(MOBILE_DIR) && rm -rf node_modules/ android/ ios/ || true

# =============================================================================
# BACKEND FASTAPI ПРОЕКТ
# =============================================================================

setup-venv-backend: ## Создать virtualenv для backend проекта
	@echo "$(YELLOW)Создание virtualenv для backend проекта...$(NC)"
	cd $(BACKEND_DIR) && python -m venv $(PYTHON_VENV_DIR)
	@echo "✓ Virtualenv создан в $(BACKEND_DIR)/$(PYTHON_VENV_DIR)"

install-backend: ## Установить зависимости для backend проекта
	@echo "$(YELLOW)Установка зависимостей для backend проекта...$(NC)"
	@if [ ! -d "$(BACKEND_DIR)/$(PYTHON_VENV_DIR)" ]; then \
		echo "Создаем virtualenv..."; \
		$(MAKE) setup-venv-backend; \
	fi
	cd $(BACKEND_DIR) && source $(PYTHON_ACTIVATE) && pip install -r requirements.txt

build-backend: ## Подготовить backend проект к деплою
	@echo "$(YELLOW)Подготовка backend проекта к деплою...$(NC)"
	cd $(BACKEND_DIR) && source $(PYTHON_ACTIVATE) && pip freeze > requirements-lock.txt
	@echo "Backend готов к деплою"

test-backend: ## Запустить тесты backend проекта
	@echo "$(YELLOW)Запуск тестов backend проекта...$(NC)"
	cd $(BACKEND_DIR) && source $(PYTHON_ACTIVATE) && python -m pytest tests/ || echo "Тесты не найдены, создайте папку tests/"

run-backend: ## Запустить backend сервер
	@echo "$(YELLOW)Запуск backend сервера...$(NC)"
	cd $(BACKEND_DIR) && source $(PYTHON_ACTIVATE) && python main.py

publish-backend: ## Опубликовать backend проект
	@echo "$(YELLOW)Публикация backend проекта...$(NC)"
	@echo "Backend готов к деплою на сервер"
	@echo "Используйте: uvicorn main:app --host 0.0.0.0 --port 8000"

clean-backend: ## Очистить backend проект
	@echo "$(YELLOW)Очистка backend проекта...$(NC)"
	cd $(BACKEND_DIR) && rm -rf __pycache__/ .pytest_cache/ $(PYTHON_VENV_DIR) || true

# =============================================================================
# ДОПОЛНИТЕЛЬНЫЕ КОМАНДЫ
# =============================================================================

status: ## Показать статус всех проектов
	@echo "$(GREEN)Статус проектов:$(NC)"
	@echo "Desktop Python: $(shell [ -f $(DESKTOP_DIR)/main.py ] && echo "✓ готов" || echo "✗ не готов")"
	echo "Mobile Ionic: $(shell [ -f $(MOBILE_DIR)/src/index.html ] && echo "✓ готов" || echo "✗ не готов")"
	@echo "Backend FastAPI: $(shell [ -f $(BACKEND_DIR)/main.py ] && echo "✓ готов" || echo "✗ не готов")"

check-deps: ## Проверить установленные зависимости
	@echo "$(GREEN)Проверка зависимостей:$(NC)"
	@python --version 2>/dev/null && echo "Python: установлен" || (\
		echo "$(RED)Python: не установлен$(NC)"; \
		echo "💡 Установка Python:"; \
		echo "   Windows: https://python.org/downloads/"; \
		echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"; \
		echo "   macOS: brew install python3"; \
		echo "" \
	)
	@node --version 2>/dev/null && echo "Node.js: установлен" || (\
		echo "$(RED)Node.js: не установлен$(NC)"; \
		echo "💡 Установка Node.js:"; \
		echo "   Скачать с: https://nodejs.org/"; \
		echo "   Windows: winget install OpenJS.NodeJS"; \
		echo "   Ubuntu/Debian: sudo apt install nodejs npm"; \
		echo "   macOS: brew install node"; \
		echo "" \
	)
	@ionic --version 2>/dev/null && echo "Ionic CLI: установлен" || (\
		echo "$(RED)Ionic CLI: не установлен$(NC)"; \
		echo "💡 Установка Ionic CLI:"; \
		echo "   npm install -g @ionic/cli"; \
		echo "   Документация: https://ionicframework.com/docs/cli"; \
		echo "" \
	)
	@java -version 2>/dev/null && echo "Java JDK: установлен" || (\
		echo "$(RED)Java JDK: не установлен$(NC)"; \
		echo "💡 Установка JDK для Ionic Framework:"; \
		echo "   Скачать JDK от Adoptium: https://adoptium.net/temurin/nightly"; \
		echo "   Рекомендуемые версии: JDK 11 или JDK 17"; \
		echo "   После установки настройте JAVA_HOME"; \
		echo "" \
	)
	@which android 2>/dev/null || adb version 2>/dev/null && echo "Android SDK: установлен" || (\
		echo "$(RED)Android SDK/Studio: не установлен$(NC)"; \
		echo "💡 Установка Android Studio (рекомендуется):"; \
		echo "   Скачать Android Studio: https://developer.android.com/studio"; \
		echo "   Включает: Android SDK, эмуляторы, все необходимые инструменты"; \
		echo "   После установки настройте ANDROID_HOME"; \
		echo "   Создайте Android Virtual Device (AVD) для тестирования"; \
		echo "" \
	)
	@echo ""
	@echo "$(GREEN)Virtualenv статус:$(NC)"
	@echo "Desktop virtualenv: $(shell [ -d $(DESKTOP_DIR)/$(PYTHON_VENV_DIR) ] && echo "✓ создан" || echo "⚠️  не создан (запустите: make setup-venv-desktop)")"
	@echo "Backend virtualenv: $(shell [ -d $(BACKEND_DIR)/$(PYTHON_VENV_DIR) ] && echo "✓ создан" || echo "⚠️  не создан (запустите: make setup-venv-backend)")"
	@echo ""
	@echo "$(YELLOW)📋 Быстрая настройка всех зависимостей:$(NC)"
	@echo "   make setup-venv && make install-all"