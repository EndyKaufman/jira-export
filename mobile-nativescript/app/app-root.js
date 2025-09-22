import { Observable, Dialogs, ObservableArray } from '@nativescript/core';

function createViewModel() {
    const viewModel = new Observable();
    
    // Поля для авторизации
    viewModel.jiraUrl = 'https://your-jira-instance.com';
    viewModel.email = '';
    viewModel.password = '';
    
    // Опции для фильтров
    viewModel.statusOptions = new ObservableArray(['Все', 'To Do', 'In Progress', 'Done', 'Backlog']);
    viewModel.priorityOptions = new ObservableArray(['Все', 'Highest', 'High', 'Medium', 'Low', 'Lowest']);
    
    // Текущие значения фильтров
    viewModel.selectedStatusIndex = 0;
    viewModel.selectedPriorityIndex = 0;
    viewModel.assigneeFilter = '';
    viewModel.searchFilter = '';
    
    // Тестовые данные для задач
    viewModel.tasks = new ObservableArray([
        {
            id: 'PROJ-123',
            title: 'Исправить ошибку в аутентификации',
            status: 'In Progress',
            priority: 'High',
            assignee: 'Иван Петров',
            updated: '2024-03-15',
            selected: false
        },
        {
            id: 'PROJ-124',
            title: 'Добавить новую функцию экспорта',
            status: 'To Do',
            priority: 'Medium',
            assignee: 'Мария Сидорова',
            updated: '2024-03-14',
            selected: false
        },
        {
            id: 'PROJ-125',
            title: 'Обновить документацию API',
            status: 'Done',
            priority: 'Low',
            assignee: 'Алексей Смирнов',
            updated: '2024-03-13',
            selected: false
        },
        {
            id: 'PROJ-126',
            title: 'Оптимизировать производительность',
            status: 'In Progress',
            priority: 'Highest',
            assignee: 'Елена Козлова',
            updated: '2024-03-12',
            selected: false
        },
        {
            id: 'PROJ-127',
            title: 'Настроить CI/CD pipeline',
            status: 'To Do',
            priority: 'High',
            assignee: 'Дмитрий Волков',
            updated: '2024-03-11',
            selected: false
        }
    ]);
    
    // Переменные для выбора задач
    viewModel.selectedTasksCount = 0;
    viewModel.allSelected = false;
    
    // Пагинация
    viewModel.currentPage = 1;
    viewModel.totalPages = 10;
    viewModel.pageInfo = `Страница ${viewModel.currentPage} из ${viewModel.totalPages}`;
    viewModel.canGoPrevious = false;
    viewModel.canGoNext = true;
    viewModel.gotoPage = '';
    
    // Функция для входа в JIRA
    viewModel.loginToJira = function() {
        if (!viewModel.jiraUrl || !viewModel.email || !viewModel.password) {
            Dialogs.alert({
                title: 'Ошибка',
                message: 'Пожалуйста, заполните все поля',
                okButtonText: 'OK'
            });
            return;
        }
        
        // Здесь будет реальная логика подключения к JIRA
        Dialogs.alert({
            title: 'Успех',
            message: `Подключение к JIRA успешно!\nURL: ${viewModel.jiraUrl}\nEmail: ${viewModel.email}`,
            okButtonText: 'OK'
        });
    };
    
    // Функция применения фильтров
    viewModel.applyFilters = function() {
        const status = viewModel.statusOptions.getItem(viewModel.selectedStatusIndex);
        const priority = viewModel.priorityOptions.getItem(viewModel.selectedPriorityIndex);
        
        // Здесь будет реальная логика фильтрации
        Dialogs.alert({
            title: 'Фильтры',
            message: `Применены фильтры:
Статус: ${status}
Приоритет: ${priority}
Исполнитель: ${viewModel.assigneeFilter}
Поиск: ${viewModel.searchFilter}`,
            okButtonText: 'OK'
        });
    };
    
    // Функция сброса фильтров
    viewModel.resetFilters = function() {
        viewModel.selectedStatusIndex = 0;
        viewModel.selectedPriorityIndex = 0;
        viewModel.assigneeFilter = '';
        viewModel.searchFilter = '';
        
        Dialogs.alert({
            title: 'Фильтры',
            message: 'Все фильтры сброшены',
            okButtonText: 'OK'
        });
    };
    
    // Обработчик нажатия на задачу
    viewModel.onTaskTap = function(args) {
        const task = viewModel.tasks.getItem(args.index);
        Dialogs.alert({
            title: `Задача ${task.id}`,
            message: `Заголовок: ${task.title}\nСтатус: ${task.status}\nПриоритет: ${task.priority}\nИсполнитель: ${task.assignee}`,
            okButtonText: 'OK'
        });
    };
    
    // Пагинация
    viewModel.previousPage = function() {
        if (viewModel.currentPage > 1) {
            viewModel.currentPage--;
            viewModel.updatePagination();
        }
    };
    
    viewModel.nextPage = function() {
        if (viewModel.currentPage < viewModel.totalPages) {
            viewModel.currentPage++;
            viewModel.updatePagination();
        }
    };
    
    viewModel.goToPage = function() {
        const page = parseInt(viewModel.gotoPage);
        if (page && page >= 1 && page <= viewModel.totalPages) {
            viewModel.currentPage = page;
            viewModel.updatePagination();
            viewModel.gotoPage = '';
        } else {
            Dialogs.alert({
                title: 'Ошибка',
                message: 'Введите корректный номер страницы',
                okButtonText: 'OK'
            });
        }
    };
    
    viewModel.updatePagination = function() {
        viewModel.set('pageInfo', `Страница ${viewModel.currentPage} из ${viewModel.totalPages}`);
        viewModel.set('canGoPrevious', viewModel.currentPage > 1);
        viewModel.set('canGoNext', viewModel.currentPage < viewModel.totalPages);
    };
    
    // Обновление данных
    viewModel.refreshData = function() {
        Dialogs.alert({
            title: 'Обновление',
            message: 'Данные обновлены',
            okButtonText: 'OK'
        });
    };
    
    // Новые функции для работы с чекбоксами и действиями
    
    // Переключение выбора одной задачи
    viewModel.toggleTaskSelection = function(args) {
        const task = args.object.bindingContext;
        task.selected = !task.selected;
        
        // Обновляем счетчик выбранных задач
        viewModel.updateSelectedCount();
    };
    
    // Массовое переключение выбора
    viewModel.toggleAllSelection = function() {
        viewModel.allSelected = !viewModel.allSelected;
        
        for (let i = 0; i < viewModel.tasks.length; i++) {
            const task = viewModel.tasks.getItem(i);
            task.selected = viewModel.allSelected;
            viewModel.tasks.setItem(i, task);
        }
        
        viewModel.updateSelectedCount();
    };
    
    // Обновление счетчика выбранных задач
    viewModel.updateSelectedCount = function() {
        let count = 0;
        for (let i = 0; i < viewModel.tasks.length; i++) {
            if (viewModel.tasks.getItem(i).selected) {
                count++;
            }
        }
        viewModel.set('selectedTasksCount', count);
    };
    
    // Очистка выбора
    viewModel.clearSelection = function() {
        for (let i = 0; i < viewModel.tasks.length; i++) {
            const task = viewModel.tasks.getItem(i);
            task.selected = false;
            viewModel.tasks.setItem(i, task);
        }
        viewModel.allSelected = false;
        viewModel.updateSelectedCount();
    };
    
    // Показ деталей задачи
    viewModel.showTaskDetails = function(args) {
        const task = args.object.bindingContext;
        
        Dialogs.alert({
            title: `Детали задачи ${task.id}`,
            message: `ID: ${task.id}
Заголовок: ${task.title}
Статус: ${task.status}
Приоритет: ${task.priority}
Исполнитель: ${task.assignee}
Обновлено: ${task.updated}`,
            okButtonText: 'Закрыть'
        });
    };
    
    // Экспорт задачи в PDF
    viewModel.exportTaskPdf = function(args) {
        const task = args.object.bindingContext;
        
        Dialogs.alert({
            title: 'Экспорт PDF',
            message: `Генерируем PDF для задачи ${task.id}...

Заголовок: ${task.title}
Статус: ${task.status}
Приоритет: ${task.priority}`,
            okButtonText: 'Готово'
        });
    };
    
    // Открытие задачи в JIRA
    viewModel.openInJira = function(args) {
        const task = args.object.bindingContext;
        const jiraUrl = viewModel.jiraUrl || 'https://your-jira-instance.com';
        const fullUrl = `${jiraUrl}/browse/${task.id}`;
        
        Dialogs.alert({
            title: 'Открытие в JIRA',
            message: `Открываем задачу ${task.id} в браузере:\n\n${fullUrl}`,
            okButtonText: 'Открыть'
        });
        
        // Здесь можно добавить логику открытия браузера
        // utils.openUrl(fullUrl);
    };
    
    // Массовый экспорт в PDF
    viewModel.bulkExportPdf = function() {
        const selectedTasks = viewModel.tasks.filter(task => task.selected);
        
        if (selectedTasks.length === 0) {
            Dialogs.alert({
                title: 'Предупреждение',
                message: 'Не выбрано ни одной задачи',
                okButtonText: 'OK'
            });
            return;
        }
        
        Dialogs.alert({
            title: 'Массовый экспорт',
            message: `Экспортируем ${selectedTasks.length} задач в PDF...\n\nЗадачи: ${selectedTasks.map(t => t.id).join(', ')}`,
            okButtonText: 'Готово'
        });
    };

    return viewModel;
}

export function onNavigatingTo(args) {
    const page = args.object;
    page.bindingContext = createViewModel();
}