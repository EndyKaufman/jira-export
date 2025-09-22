from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime

# Модели данных
class LoginRequest(BaseModel):
    jira_url: str
    email: str
    password: str

class Task(BaseModel):
    id: str
    title: str
    status: str
    priority: str
    assignee: str
    updated: str
    selected: bool = False

class TaskAction(BaseModel):
    task_id: str
    action_type: str  # "details", "pdf", "jira"

class BulkActionRequest(BaseModel):
    task_ids: List[str]
    action_type: str  # "pdf_export", "jira_open", "status_update"
    
class TaskSelectionRequest(BaseModel):
    task_ids: List[str]
    selected: bool

class TasksResponse(BaseModel):
    tasks: List[Task]
    current_page: int
    total_pages: int
    total_tasks: int

class FilterRequest(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee: Optional[str] = None
    search: Optional[str] = None
    page: int = 1
    per_page: int = 20

# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="JIRA Export API",
    description="REST API для работы с JIRA - вход, фильтрация задач и экспорт в PDF",
    version="1.0.0"
)

# Настройка CORS для возможности обращения с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене следует указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Тестовые данные
TEST_TASKS = [
    Task(
        id="PROJ-123",
        title="Исправить ошибку в аутентификации",
        status="In Progress",
        priority="High",
        assignee="Иван Петров",
        updated="2024-03-15",
        selected=False
    ),
    Task(
        id="PROJ-124",
        title="Добавить новую функцию экспорта",
        status="To Do",
        priority="Medium",
        assignee="Мария Сидорова",
        updated="2024-03-14",
        selected=False
    ),
    Task(
        id="PROJ-125",
        title="Обновить документацию API",
        status="Done",
        priority="Low",
        assignee="Алексей Смирнов",
        updated="2024-03-13",
        selected=False
    ),
    Task(
        id="PROJ-126",
        title="Оптимизировать производительность",
        status="In Progress",
        priority="Highest",
        assignee="Елена Козлова",
        updated="2024-03-12",
        selected=False
    ),
    Task(
        id="PROJ-127",
        title="Настроить CI/CD pipeline",
        status="To Do",
        priority="High",
        assignee="Дмитрий Волков",
        updated="2024-03-11",
        selected=False
    ),
    Task(
        id="PROJ-128",
        title="Рефакторинг легаси кода",
        status="Backlog",
        priority="Medium",
        assignee="Ольга Новикова",
        updated="2024-03-10",
        selected=False
    ),
    Task(
        id="PROJ-129",
        title="Написать тесты для API",
        status="Done",
        priority="High",
        assignee="Павел Казаков",
        updated="2024-03-09",
        selected=False
    ),
    Task(
        id="PROJ-130",
        title="Обновить дизайн систему",
        status="In Progress",
        priority="Low",
        assignee="Анна Лебедева",
        updated="2024-03-08",
        selected=False
    )
]

@app.get("/")
async def root():
    """
    Корневой эндпоинт API
    """
    return {
        "message": "JIRA Export API работает!",
        "available_endpoints": [
            "/auth/login - Вход в JIRA",
            "/tasks - Получение списка задач",
            "/tasks/filter - Фильтрация задач",
            "/tasks/{task_id} - Получение деталей задачи",
            "/tasks/{task_id}/export-pdf - Экспорт задачи в PDF",
            "/tasks/bulk/export-pdf - Массовый экспорт в PDF",
            "/tasks/selection - Управление выбором задач",
            "/tasks/{task_id}/action - Выполнение действия над задачей",
            "/health - Проверка здоровья API"
        ]
    }

@app.post("/auth/login")
async def login_to_jira(login_data: LoginRequest):
    """
    Аутентификация в JIRA
    """
    # Проверка обязательных полей
    if not login_data.jira_url or not login_data.email or not login_data.password:
        raise HTTPException(
            status_code=400,
            detail="Не заполнены обязательные поля: URL, email, password"
        )
    
    # Здесь будет реальная логика подключения к JIRA API
    return {
        "status": "success",
        "message": "Подключение к JIRA успешно!",
        "jira_url": login_data.jira_url,
        "email": login_data.email,
        "authenticated_at": datetime.now().isoformat()
    }

@app.get("/tasks", response_model=TasksResponse)
async def get_tasks(page: int = 1, per_page: int = 20):
    """
    Получение списка задач с пагинацией
    """
    total_tasks = len(TEST_TASKS)
    total_pages = (total_tasks + per_page - 1) // per_page
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    tasks_page = TEST_TASKS[start_idx:end_idx]
    
    return TasksResponse(
        tasks=tasks_page,
        current_page=page,
        total_pages=total_pages,
        total_tasks=total_tasks
    )

@app.post("/tasks/filter", response_model=TasksResponse)
async def filter_tasks(filter_request: FilterRequest):
    """
    Фильтрация задач по различным критериям
    """
    filtered_tasks = TEST_TASKS.copy()
    
    # Фильтрация по статусу
    if filter_request.status and filter_request.status != "Все":
        filtered_tasks = [task for task in filtered_tasks if task.status == filter_request.status]
    
    # Фильтрация по приоритету
    if filter_request.priority and filter_request.priority != "Все":
        filtered_tasks = [task for task in filtered_tasks if task.priority == filter_request.priority]
    
    # Фильтрация по исполнителю
    if filter_request.assignee:
        filtered_tasks = [task for task in filtered_tasks if filter_request.assignee.lower() in task.assignee.lower()]
    
    # Поиск по тексту
    if filter_request.search:
        search_term = filter_request.search.lower()
        filtered_tasks = [task for task in filtered_tasks 
                         if search_term in task.title.lower() or search_term in task.id.lower()]
    
    # Пагинация
    total_tasks = len(filtered_tasks)
    total_pages = (total_tasks + filter_request.per_page - 1) // filter_request.per_page
    
    start_idx = (filter_request.page - 1) * filter_request.per_page
    end_idx = start_idx + filter_request.per_page
    
    tasks_page = filtered_tasks[start_idx:end_idx]
    
    return TasksResponse(
        tasks=tasks_page,
        current_page=filter_request.page,
        total_pages=total_pages,
        total_tasks=total_tasks
    )

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task_details(task_id: str):
    """
    Получение деталей конкретной задачи
    """
    task = next((task for task in TEST_TASKS if task.id == task_id), None)
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Задача с ID {task_id} не найдена"
        )
    
    return task

@app.post("/tasks/{task_id}/export-pdf")
async def export_task_to_pdf(task_id: str):
    """
    Экспорт задачи в PDF формат
    """
    task = next((task for task in TEST_TASKS if task.id == task_id), None)
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Задача с ID {task_id} не найдена"
        )
    
    # Здесь будет реальная логика генерации PDF
    return {
        "status": "success",
        "message": f"PDF для задачи {task_id} сгенерирован",
        "task_id": task_id,
        "task_title": task.title,
        "pdf_url": f"/downloads/task_{task_id}.pdf",
        "generated_at": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """
    Проверка состояния API
    """
    return {
        "status": "healthy", 
        "message": "JIRA Export API работает корректно",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "endpoints_count": 6
    }

@app.get("/status/tasks")
async def get_tasks_status():
    """
    Статистика по задачам
    """
    status_stats = {}
    priority_stats = {}
    
    for task in TEST_TASKS:
        # Статистика по статусам
        status_stats[task.status] = status_stats.get(task.status, 0) + 1
        # Статистика по приоритетам
        priority_stats[task.priority] = priority_stats.get(task.priority, 0) + 1
    
    return {
        "total_tasks": len(TEST_TASKS),
        "status_breakdown": status_stats,
        "priority_breakdown": priority_stats,
        "last_updated": max(task.updated for task in TEST_TASKS)
    }

# Новые эндпоинты для работы с чекбоксами и действиями

@app.post("/tasks/selection")
async def update_task_selection(selection_request: TaskSelectionRequest):
    """
    Обновление состояния выбора задач
    """
    updated_tasks = []
    
    for task in TEST_TASKS:
        if task.id in selection_request.task_ids:
            task.selected = selection_request.selected
            updated_tasks.append(task.id)
    
    return {
        "status": "success",
        "message": f"Обновлено состояние выбора для {len(updated_tasks)} задач",
        "updated_tasks": updated_tasks,
        "selected": selection_request.selected
    }

@app.get("/tasks/selected")
async def get_selected_tasks():
    """
    Получение списка выбранных задач
    """
    selected_tasks = [task for task in TEST_TASKS if task.selected]
    
    return {
        "selected_tasks": selected_tasks,
        "selected_count": len(selected_tasks),
        "total_count": len(TEST_TASKS)
    }

@app.post("/tasks/{task_id}/action")
async def perform_task_action(task_id: str, action: TaskAction):
    """
    Выполнение действия над задачей
    """
    task = next((task for task in TEST_TASKS if task.id == task_id), None)
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Задача с ID {task_id} не найдена"
        )
    
    if action.action_type == "details":
        return {
            "status": "success",
            "action": "details",
            "task": task,
            "message": f"Получены детали задачи {task_id}"
        }
    elif action.action_type == "pdf":
        return {
            "status": "success",
            "action": "pdf_export",
            "task_id": task_id,
            "task_title": task.title,
            "pdf_url": f"/downloads/task_{task_id}.pdf",
            "generated_at": datetime.now().isoformat(),
            "message": f"PDF для задачи {task_id} сгенерирован"
        }
    elif action.action_type == "jira":
        jira_url = f"https://your-jira-instance.com/browse/{task_id}"
        return {
            "status": "success",
            "action": "jira_link",
            "task_id": task_id,
            "jira_url": jira_url,
            "message": f"Ссылка на задачу {task_id} в JIRA"
        }
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Неизвестный тип действия: {action.action_type}"
        )

@app.post("/tasks/bulk/export-pdf")
async def bulk_export_pdf(bulk_request: BulkActionRequest):
    """
    Массовый экспорт задач в PDF
    """
    if bulk_request.action_type != "pdf_export":
        raise HTTPException(
            status_code=400,
            detail="Данный эндпоинт поддерживает только экспорт PDF"
        )
    
    # Находим задачи по ID
    tasks_to_export = [task for task in TEST_TASKS if task.id in bulk_request.task_ids]
    
    if not tasks_to_export:
        raise HTTPException(
            status_code=404,
            detail="Не найдено задач для экспорта"
        )
    
    exported_files = []
    for task in tasks_to_export:
        exported_files.append({
            "task_id": task.id,
            "task_title": task.title,
            "pdf_url": f"/downloads/task_{task.id}.pdf"
        })
    
    return {
        "status": "success",
        "action": "bulk_pdf_export",
        "exported_count": len(exported_files),
        "total_requested": len(bulk_request.task_ids),
        "exported_files": exported_files,
        "generated_at": datetime.now().isoformat(),
        "message": f"Экспортировано {len(exported_files)} задач в PDF"
    }

@app.post("/tasks/bulk/clear-selection")
async def clear_all_selection():
    """
    Очистка выбора всех задач
    """
    cleared_count = 0
    for task in TEST_TASKS:
        if task.selected:
            task.selected = False
            cleared_count += 1
    
    return {
        "status": "success",
        "message": f"Очищен выбор для {cleared_count} задач",
        "cleared_count": cleared_count
    }

@app.post("/tasks/bulk/toggle-all")
async def toggle_all_selection():
    """
    Переключение выбора всех задач
    """
    # Проверяем, все ли задачи выбраны
    all_selected = all(task.selected for task in TEST_TASKS)
    
    # Переключаем состояние
    new_selection_state = not all_selected
    changed_count = 0
    
    for task in TEST_TASKS:
        if task.selected != new_selection_state:
            task.selected = new_selection_state
            changed_count += 1
    
    return {
        "status": "success",
        "message": f"{'Выбраны' if new_selection_state else 'Отменен выбор'} все задачи",
        "new_state": new_selection_state,
        "changed_count": changed_count,
        "total_tasks": len(TEST_TASKS)
    }

if __name__ == "__main__":
    # Запуск сервера для разработки
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Автоматическая перезагрузка при изменении кода
        log_level="info"
    )