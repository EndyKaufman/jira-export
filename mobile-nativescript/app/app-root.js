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
            updated: '2024-03-15'
        },
        {
            id: 'PROJ-124',
            title: 'Добавить новую функцию экспорта',
            status: 'To Do',
            priority: 'Medium',
            assignee: 'Мария Сидорова',
            updated: '2024-03-14'
        },
        {
            id: 'PROJ-125',
            title: 'Обновить документацию API',
            status: 'Done',
            priority: 'Low',
            assignee: 'Алексей Смирнов',
            updated: '2024-03-13'
        },
        {
            id: 'PROJ-126',
            title: 'Оптимизировать производительность',
            status: 'In Progress',
            priority: 'Highest',
            assignee: 'Елена Козлова',
            updated: '2024-03-12'
        },
        {
            id: 'PROJ-127',
            title: 'Настроить CI/CD pipeline',
            status: 'To Do',
            priority: 'High',
            assignee: 'Дмитрий Волков',
            updated: '2024-03-11'
        }
    ]);
    
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

    return viewModel;
}

export function onNavigatingTo(args) {
    const page = args.object;
    page.bindingContext = createViewModel();
}