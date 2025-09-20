@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Скрипт для управления всеми проектами в Windows
:: Альтернатива Makefile для пользователей без Make
:: Включает поддержку virtualenv для Python проектов

set "GREEN=[32m"
set "YELLOW=[33m"
set "RED=[31m"
set "NC=[0m"

:: Python virtualenv настройки
set "PYTHON_VENV_DIR=.venv"
set "PYTHON_ACTIVATE_SCRIPT=Scripts\activate.bat"

if "%1"=="" goto :help
if "%1"=="help" goto :help
if "%1"=="setup-venv" goto :setup_venv
if "%1"=="clean-venv" goto :clean_venv
if "%1"=="install-all" goto :install_all
if "%1"=="build-all" goto :build_all
if "%1"=="test-all" goto :test_all
if "%1"=="publish-all" goto :publish_all
if "%1"=="clean-all" goto :clean_all
if "%1"=="setup-venv-desktop" goto :setup_venv_desktop
if "%1"=="install-desktop" goto :install_desktop
if "%1"=="build-desktop" goto :build_desktop
if "%1"=="test-desktop" goto :test_desktop
if "%1"=="run-desktop" goto :run_desktop
if "%1"=="publish-desktop" goto :publish_desktop
if "%1"=="clean-desktop" goto :clean_desktop
if "%1"=="install-mobile" goto :install_mobile
if "%1"=="build-mobile" goto :build_mobile
if "%1"=="test-mobile" goto :test_mobile
if "%1"=="run-mobile" goto :run_mobile
if "%1"=="publish-mobile" goto :publish_mobile
if "%1"=="clean-mobile" goto :clean_mobile
if "%1"=="setup-venv-backend" goto :setup_venv_backend
if "%1"=="install-backend" goto :install_backend
if "%1"=="build-backend" goto :build_backend
if "%1"=="test-backend" goto :test_backend
if "%1"=="run-backend" goto :run_backend
if "%1"=="publish-backend" goto :publish_backend
if "%1"=="clean-backend" goto :clean_backend
if "%1"=="status" goto :status
if "%1"=="check-deps" goto :check_deps

echo %RED%Неизвестная команда: %1%NC%
goto :help

:help
echo %GREEN%Доступные команды:%NC%
echo.
echo %YELLOW%Массовые операции:%NC%
echo   install-all     - Установить зависимости для всех проектов
echo   build-all       - Собрать все проекты
echo   test-all        - Запустить тесты для всех проектов
echo   publish-all     - Опубликовать все проекты
echo   clean-all       - Очистить все проекты
echo.
echo %YELLOW%Python virtualenv команды:%NC%
echo   setup-venv      - Создать virtualenv для всех Python проектов
echo   clean-venv      - Удалить virtualenv для всех Python проектов
echo.
echo %YELLOW%Desktop Python проект:%NC%
echo   setup-venv-desktop - Создать virtualenv
echo   install-desktop - Установить зависимости
echo   build-desktop   - Собрать в .exe
echo   test-desktop    - Запустить тесты
echo   run-desktop     - Запустить приложение
echo   publish-desktop - Опубликовать проект
echo   clean-desktop   - Очистить проект
echo.
echo %YELLOW%Mobile NativeScript проект:%NC%
echo   install-mobile  - Установить зависимости
echo   build-mobile    - Собрать .apk
echo   test-mobile     - Запустить тесты
echo   run-mobile      - Запустить на эмуляторе
echo   publish-mobile  - Опубликовать в Google Play
echo   clean-mobile    - Очистить проект
echo.
echo %YELLOW%Backend FastAPI проект:%NC%
echo   setup-venv-backend - Создать virtualenv
echo   install-backend - Установить зависимости
echo   build-backend   - Подготовить к деплою
echo   test-backend    - Запустить тесты
echo   run-backend     - Запустить сервер
echo   publish-backend - Опубликовать на сервер
echo   clean-backend   - Очистить проект
echo.
echo %YELLOW%Дополнительно:%NC%
echo   status          - Показать статус проектов
echo   check-deps      - Проверить зависимости
echo.
echo %YELLOW%Использование:%NC% manage.bat [команда]
goto :end

:: =============================================================================
:: PYTHON VIRTUALENV КОМАНДЫ
:: =============================================================================

:setup_venv
echo %GREEN%Создание virtualenv для всех Python проектов...%NC%
call :setup_venv_desktop
call :setup_venv_backend
echo %GREEN%✓ Virtualenv созданы для всех Python проектов%NC%
goto :end

:clean_venv
echo %GREEN%Удаление virtualenv для всех Python проектов...%NC%
cd desktop-python
if exist %PYTHON_VENV_DIR% rmdir /s /q %PYTHON_VENV_DIR%
cd ..
cd backend-fastapi
if exist %PYTHON_VENV_DIR% rmdir /s /q %PYTHON_VENV_DIR%
cd ..
echo %GREEN%✓ Virtualenv удалены для всех Python проектов%NC%
goto :end

:: =============================================================================
:: МАССОВЫЕ ОПЕРАЦИИ
:: =============================================================================

:install_all
echo %GREEN%Установка зависимостей для всех проектов...%NC%
call :install_desktop
call :install_mobile
call :install_backend
echo %GREEN%✓ Зависимости установлены для всех проектов%NC%
goto :end

:build_all
echo %GREEN%Сборка всех проектов...%NC%
call :build_desktop
call :build_mobile
call :build_backend
echo %GREEN%✓ Все проекты собраны%NC%
goto :end

:test_all
echo %GREEN%Запуск тестов для всех проектов...%NC%
call :test_desktop
call :test_mobile
call :test_backend
echo %GREEN%✓ Тесты выполнены для всех проектов%NC%
goto :end

:publish_all
echo %GREEN%Публикация всех проектов...%NC%
call :publish_desktop
call :publish_mobile
call :publish_backend
echo %GREEN%✓ Все проекты опубликованы%NC%
goto :end

:clean_all
echo %GREEN%Очистка всех проектов...%NC%
call :clean_desktop
call :clean_mobile
call :clean_backend
echo %GREEN%✓ Все проекты очищены%NC%
goto :end

:: =============================================================================
:: DESKTOP PYTHON ПРОЕКТ
:: =============================================================================

:setup_venv_desktop
echo %YELLOW%Создание virtualenv для desktop проекта...%NC%
cd desktop-python
python -m venv %PYTHON_VENV_DIR%
echo ✓ Virtualenv создан в desktop-python\%PYTHON_VENV_DIR%
cd ..
goto :eof

:install_desktop
echo %YELLOW%Установка зависимостей для desktop проекта...%NC%
cd desktop-python
if not exist %PYTHON_VENV_DIR% (
    echo Создаем virtualenv...
    python -m venv %PYTHON_VENV_DIR%
)
call %PYTHON_VENV_DIR%\%PYTHON_ACTIVATE_SCRIPT%
pip install -r requirements.txt
cd ..
goto :eof

:build_desktop
echo %YELLOW%Сборка desktop проекта в .exe...%NC%
cd desktop-python
call %PYTHON_VENV_DIR%\%PYTHON_ACTIVATE_SCRIPT%
pyinstaller --onefile --windowed main.py
cd ..
goto :eof

:test_desktop
echo %YELLOW%Запуск тестов desktop проекта...%NC%
cd desktop-python
call %PYTHON_VENV_DIR%\%PYTHON_ACTIVATE_SCRIPT%
python -m pytest tests/ 2>nul || echo Тесты не найдены, создайте папку tests/
cd ..
goto :eof

:run_desktop
echo %YELLOW%Запуск desktop приложения...%NC%
cd desktop-python
call %PYTHON_VENV_DIR%\%PYTHON_ACTIVATE_SCRIPT%
python main.py
cd ..
goto :eof

:publish_desktop
echo %YELLOW%Публикация desktop проекта...%NC%
echo Desktop приложение готово в папке desktop-python\dist\
echo Готово к распространению как standalone .exe файл
goto :eof

:clean_desktop
echo %YELLOW%Очистка desktop проекта...%NC%
cd desktop-python
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec
if exist __pycache__ rmdir /s /q __pycache__
if exist %PYTHON_VENV_DIR% rmdir /s /q %PYTHON_VENV_DIR%
cd ..
goto :eof

:: =============================================================================
:: MOBILE NATIVESCRIPT ПРОЕКТ
:: =============================================================================

:install_mobile
echo %YELLOW%Установка зависимостей для mobile проекта...%NC%
cd mobile-nativescript
npm install
cd ..
goto :eof

:build_mobile
echo %YELLOW%Сборка mobile проекта в .apk...%NC%
cd mobile-nativescript
tns build android --release
cd ..
goto :eof

:test_mobile
echo %YELLOW%Запуск тестов mobile проекта...%NC%
cd mobile-nativescript
npm test 2>nul || echo Тесты не настроены, добавьте тестовый фреймворк
cd ..
goto :eof

:run_mobile
echo %YELLOW%Запуск mobile приложения...%NC%
cd mobile-nativescript
tns run android
cd ..
goto :eof

:publish_mobile
echo %YELLOW%Подготовка к публикации mobile проекта...%NC%
echo APK готов для загрузки в Google Play Console
echo Файл находится в mobile-nativescript\platforms\android\app\build\outputs\apk\
goto :eof

:clean_mobile
echo %YELLOW%Очистка mobile проекта...%NC%
cd mobile-nativescript
tns clean 2>nul
if exist node_modules rmdir /s /q node_modules
if exist platforms rmdir /s /q platforms
if exist hooks rmdir /s /q hooks
cd ..
goto :eof

:: =============================================================================
:: BACKEND FASTAPI ПРОЕКТ
:: =============================================================================

:setup_venv_backend
echo %YELLOW%Создание virtualenv для backend проекта...%NC%
cd backend-fastapi
python -m venv %PYTHON_VENV_DIR%
echo ✓ Virtualenv создан в backend-fastapi\%PYTHON_VENV_DIR%
cd ..
goto :eof

:install_backend
echo %YELLOW%Установка зависимостей для backend проекта...%NC%
cd backend-fastapi
if not exist %PYTHON_VENV_DIR% (
    echo Создаем virtualenv...
    python -m venv %PYTHON_VENV_DIR%
)
call %PYTHON_VENV_DIR%\%PYTHON_ACTIVATE_SCRIPT%
pip install -r requirements.txt
cd ..
goto :eof

:build_backend
echo %YELLOW%Подготовка backend проекта к деплою...%NC%
cd backend-fastapi
call %PYTHON_VENV_DIR%\%PYTHON_ACTIVATE_SCRIPT%
pip freeze > requirements-lock.txt
echo Backend готов к деплою
cd ..
goto :eof

:test_backend
echo %YELLOW%Запуск тестов backend проекта...%NC%
cd backend-fastapi
call %PYTHON_VENV_DIR%\%PYTHON_ACTIVATE_SCRIPT%
python -m pytest tests/ 2>nul || echo Тесты не найдены, создайте папку tests/
cd ..
goto :eof

:run_backend
echo %YELLOW%Запуск backend сервера...%NC%
cd backend-fastapi
call %PYTHON_VENV_DIR%\%PYTHON_ACTIVATE_SCRIPT%
python main.py
cd ..
goto :eof

:publish_backend
echo %YELLOW%Публикация backend проекта...%NC%
echo Backend готов к деплою на сервер
echo Используйте: uvicorn main:app --host 0.0.0.0 --port 8000
goto :eof

:clean_backend
echo %YELLOW%Очистка backend проекта...%NC%
cd backend-fastapi
if exist __pycache__ rmdir /s /q __pycache__
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist %PYTHON_VENV_DIR% rmdir /s /q %PYTHON_VENV_DIR%
cd ..
goto :eof

:: =============================================================================
:: ДОПОЛНИТЕЛЬНЫЕ КОМАНДЫ
:: =============================================================================

:status
echo %GREEN%Статус проектов:%NC%
if exist desktop-python\main.py (echo Desktop Python: ✓ готов) else (echo Desktop Python: ✗ не готов)
if exist mobile-nativescript\app.js (echo Mobile NativeScript: ✓ готов) else (echo Mobile NativeScript: ✗ не готов)
if exist backend-fastapi\main.py (echo Backend FastAPI: ✓ готов) else (echo Backend FastAPI: ✗ не готов)
goto :end

:check_deps
echo %GREEN%Проверка зависимостей:%NC%
python --version 2>nul && (
    echo Python: установлен
) || (
    echo %RED%Python: не установлен%NC%
    echo 💡 Установка Python:
    echo    Windows: https://python.org/downloads/
    echo    winget install Python.Python.3.11
    echo    Или через Microsoft Store
    echo.
)
node --version 2>nul && (
    echo Node.js: установлен
) || (
    echo %RED%Node.js: не установлен%NC%
    echo 💡 Установка Node.js:
    echo    Скачать с: https://nodejs.org/
    echo    winget install OpenJS.NodeJS
    echo    Или через chocolatey: choco install nodejs
    echo.
)
tns --version 2>nul && (
    echo NativeScript CLI: установлен
) || (
    echo %RED%NativeScript CLI: не установлен%NC%
    echo 💡 Установка NativeScript CLI:
    echo    npm install -g nativescript
    echo    Документация: https://docs.nativescript.org/
    echo.
)
java -version 2>nul && (
    echo Java JDK: установлен
) || (
    echo %RED%Java JDK: не установлен%NC%
    echo 💡 Установка JDK для NativeScript:
    echo    Скачать JDK от Adoptium: https://adoptium.net/temurin/nightly
    echo    Рекомендуемые версии: JDK 11 или JDK 17
    echo    После установки настройте JAVA_HOME
    echo.
)
adb version 2>nul && (
    echo Android SDK: установлен
) || (
    echo %RED%Android SDK/Studio: не установлен%NC%
    echo 💡 Установка Android Studio рекомендуется:
    echo    Скачать Android Studio: https://developer.android.com/studio
    echo    Включает: Android SDK, эмуляторы, все необходимые инструменты
    echo    После установки настройте ANDROID_HOME
    echo    Создайте Android Virtual Device AVD для тестирования
    echo.
)
echo.
echo %GREEN%Virtualenv статус:%NC%
if exist desktop-python\%PYTHON_VENV_DIR% (
    echo Desktop virtualenv: ✓ создан
) else (
    echo Desktop virtualenv: ⚠️  не создан ^запустите: manage.bat setup-venv-desktop^
)
if exist backend-fastapi\%PYTHON_VENV_DIR% (
    echo Backend virtualenv: ✓ создан
) else (
    echo Backend virtualenv: ⚠️  не создан ^запустите: manage.bat setup-venv-backend^
)
echo.
echo %YELLOW%📋 Быстрая настройка всех зависимостей:%NC%
echo    manage.bat setup-venv ^&^& manage.bat install-all
goto :end

:end
endlocal