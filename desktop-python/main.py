import tkinter as tk
from tkinter import messagebox, ttk

class JiraExportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JIRA Export - Десктопное приложение")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Создаем панель с табами
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Создаем вкладки
        self.create_login_tab()
        self.create_tasks_tab()
    
    def create_login_tab(self):
        """Создает вкладку для входа в JIRA"""
        login_frame = ttk.Frame(self.notebook)
        self.notebook.add(login_frame, text="Вход в JIRA")
        
        # Главный контейнер для центрирования
        main_container = tk.Frame(login_frame)
        main_container.pack(expand=True, fill='both')
        
        # Фрейм с полями ввода
        form_frame = tk.Frame(main_container, padx=50, pady=50)
        form_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Заголовок
        title_label = tk.Label(
            form_frame,
            text="Подключение к JIRA",
            font=("Arial", 16, "bold"),
            fg='darkblue'
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Поле URL
        tk.Label(form_frame, text="URL JIRA:", font=("Arial", 10)).grid(row=1, column=0, sticky='e', padx=(0, 10), pady=5)
        self.url_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.url_entry.grid(row=1, column=1, pady=5)
        self.url_entry.insert(0, "https://your-jira-instance.com")
        
        # Поле Email
        tk.Label(form_frame, text="Email:", font=("Arial", 10)).grid(row=2, column=0, sticky='e', padx=(0, 10), pady=5)
        self.email_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.email_entry.grid(row=2, column=1, pady=5)
        
        # Поле Password
        tk.Label(form_frame, text="Пароль:", font=("Arial", 10)).grid(row=3, column=0, sticky='e', padx=(0, 10), pady=5)
        self.password_entry = tk.Entry(form_frame, width=30, show='*', font=("Arial", 10))
        self.password_entry.grid(row=3, column=1, pady=5)
        
        # Кнопка входа
        login_button = tk.Button(
            form_frame,
            text="Войти",
            command=self.login_to_jira,
            font=("Arial", 12, "bold"),
            bg='#4CAF50',
            fg='white',
            padx=30,
            pady=10,
            relief='raised',
            bd=2
        )
        login_button.grid(row=4, column=0, columnspan=2, pady=20)
    
    def create_tasks_tab(self):
        """Создает вкладку для работы с задачами"""
        tasks_frame = ttk.Frame(self.notebook)
        self.notebook.add(tasks_frame, text="Задачи JIRA")
        
        # Создаем три горизонтальные панели
        # Панель 1: Фильтры (сверху)
        filters_frame = tk.Frame(tasks_frame, bg='lightgray', relief='sunken', bd=2)
        filters_frame.pack(side='top', fill='x', padx=5, pady=(5, 2))
        
        # Панель 2: Таблица с задачами (в центре)
        table_frame = tk.Frame(tasks_frame, bg='white', relief='sunken', bd=2)
        table_frame.pack(side='top', fill='both', expand=True, padx=5, pady=2)
        
        # Панель 3: Пагинация (снизу)
        pagination_frame = tk.Frame(tasks_frame, bg='lightblue', relief='sunken', bd=2)
        pagination_frame.pack(side='bottom', fill='x', padx=5, pady=(2, 5))
        
        self.create_filters_panel(filters_frame)
        self.create_table_panel(table_frame)
        self.create_pagination_panel(pagination_frame)
    
    def create_filters_panel(self, parent):
        """Создает панель с основными фильтрами"""
        # Заголовок панели
        tk.Label(parent, text="Фильтры", font=("Arial", 12, "bold"), bg='lightgray').pack(side='left', padx=20)
        
        # Создаем фрейм для горизонтального расположения фильтров
        filters_container = tk.Frame(parent, bg='lightgray')
        filters_container.pack(side='left', fill='x', expand=True, padx=10, pady=10)
        
        # Фильтр по статусу
        status_frame = tk.Frame(filters_container, bg='lightgray')
        status_frame.pack(side='left', padx=10)
        tk.Label(status_frame, text="Статус:", font=("Arial", 10), bg='lightgray').pack()
        self.status_var = tk.StringVar(value="Все")
        status_combo = ttk.Combobox(status_frame, textvariable=self.status_var, width=12)
        status_combo['values'] = ("Все", "To Do", "In Progress", "Done", "Backlog")
        status_combo.pack(pady=5)
        
        # Фильтр по приоритету
        priority_frame = tk.Frame(filters_container, bg='lightgray')
        priority_frame.pack(side='left', padx=10)
        tk.Label(priority_frame, text="Приоритет:", font=("Arial", 10), bg='lightgray').pack()
        self.priority_var = tk.StringVar(value="Все")
        priority_combo = ttk.Combobox(priority_frame, textvariable=self.priority_var, width=12)
        priority_combo['values'] = ("Все", "Highest", "High", "Medium", "Low", "Lowest")
        priority_combo.pack(pady=5)
        
        # Фильтр по исполнителю
        assignee_frame = tk.Frame(filters_container, bg='lightgray')
        assignee_frame.pack(side='left', padx=10)
        tk.Label(assignee_frame, text="Исполнитель:", font=("Arial", 10), bg='lightgray').pack()
        self.assignee_entry = tk.Entry(assignee_frame, width=15, font=("Arial", 9))
        self.assignee_entry.pack(pady=5)
        
        # Поиск по тексту
        search_frame = tk.Frame(filters_container, bg='lightgray')
        search_frame.pack(side='left', padx=10)
        tk.Label(search_frame, text="Поиск:", font=("Arial", 10), bg='lightgray').pack()
        self.search_entry = tk.Entry(search_frame, width=15, font=("Arial", 9))
        self.search_entry.pack(pady=5)
        
        # Кнопки управления
        buttons_frame = tk.Frame(filters_container, bg='lightgray')
        buttons_frame.pack(side='right', padx=20)
        
        # Кнопка применения фильтров
        filter_button = tk.Button(
            buttons_frame,
            text="Применить",
            command=self.apply_filters,
            font=("Arial", 10),
            bg='#2196F3',
            fg='white',
            padx=15,
            pady=5
        )
        filter_button.pack(side='left', padx=5)
        
        # Кнопка сброса фильтров
        reset_button = tk.Button(
            buttons_frame,
            text="Сбросить",
            command=self.reset_filters,
            font=("Arial", 10),
            bg='#FF9800',
            fg='white',
            padx=15,
            pady=5
        )
        reset_button.pack(side='left', padx=5)
    
    def create_table_panel(self, parent):
        """Создает панель с таблицей задач"""
        # Заголовок панели
        header_frame = tk.Frame(parent, bg='white')
        header_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(header_frame, text="Список задач JIRA", font=("Arial", 12, "bold"), bg='white').pack(side='left')
        
        # Кнопки для работы с выделенными элементами
        selected_actions_frame = tk.Frame(header_frame, bg='white')
        selected_actions_frame.pack(side='right')
        
        tk.Button(
            selected_actions_frame,
            text="Массовый PDF",
            command=self.bulk_export_pdf,
            font=("Arial", 9),
            bg='#FF6B6B',
            fg='white',
            padx=10
        ).pack(side='left', padx=5)
        
        tk.Button(
            selected_actions_frame,
            text="Снять выделение",
            command=self.clear_selection,
            font=("Arial", 9),
            bg='#95A5A6',
            fg='white',
            padx=10
        ).pack(side='left', padx=5)
        
        # Создаем контейнер для таблицы
        table_container = tk.Frame(parent, bg='white')
        table_container.pack(fill='both', expand=True, padx=10, pady=(5, 10))
        
        # Создаем Treeview для таблицы с чекбоксами и действиями
        columns = ("Выбрать", "ID", "Заголовок", "Статус", "Приоритет", "Исполнитель", "Обновлено", "Действия")
        self.tasks_tree = ttk.Treeview(table_container, columns=columns, show='headings', height=15)
        
        # Настраиваем заголовки столбцов
        self.tasks_tree.heading("Выбрать", text="☐ Все", command=self.toggle_all_selection)
        self.tasks_tree.heading("ID", text="ID")
        self.tasks_tree.heading("Заголовок", text="Заголовок")
        self.tasks_tree.heading("Статус", text="Статус")
        self.tasks_tree.heading("Приоритет", text="Приоритет")
        self.tasks_tree.heading("Исполнитель", text="Исполнитель")
        self.tasks_tree.heading("Обновлено", text="Обновлено")
        self.tasks_tree.heading("Действия", text="Действия")
        
        # Настраиваем ширину столбцов
        self.tasks_tree.column("Выбрать", width=60, minwidth=60)
        self.tasks_tree.column("ID", width=80, minwidth=60)
        self.tasks_tree.column("Заголовок", width=200, minwidth=150)
        self.tasks_tree.column("Статус", width=100, minwidth=80)
        self.tasks_tree.column("Приоритет", width=80, minwidth=60)
        self.tasks_tree.column("Исполнитель", width=120, minwidth=80)
        self.tasks_tree.column("Обновлено", width=100, minwidth=80)
        self.tasks_tree.column("Действия", width=200, minwidth=150)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(table_container, orient='vertical', command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем элементы
        self.tasks_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Привязываем обработчики событий
        self.tasks_tree.bind('<Double-1>', self.on_task_double_click)
        self.tasks_tree.bind('<Button-1>', self.on_task_click)
        
        # Инициализация переменных для чекбоксов
        self.selected_tasks = set()
        self.all_selected = False
        
        # Добавляем тестовые данные
        self.populate_test_data()
    
    def create_pagination_panel(self, parent):
        """Создает панель пагинации"""
        # Заголовок панели
        tk.Label(parent, text="Пагинация и управление", font=("Arial", 12, "bold"), bg='lightblue').pack(side='left', padx=20)
        
        # Создаем контейнер для элементов пагинации
        pagination_container = tk.Frame(parent, bg='lightblue')
        pagination_container.pack(side='left', fill='x', expand=True, padx=10, pady=10)
        
        # Информация о текущей странице
        info_frame = tk.Frame(pagination_container, bg='lightblue')
        info_frame.pack(side='left', padx=10)
        self.page_info_label = tk.Label(
            info_frame, 
            text="Страница 1 из 10", 
            font=("Arial", 10), 
            bg='lightblue'
        )
        self.page_info_label.pack()
        
        # Кнопки навигации
        nav_frame = tk.Frame(pagination_container, bg='lightblue')
        nav_frame.pack(side='left', padx=10)
        
        self.prev_button = tk.Button(
            nav_frame,
            text="◀ Пред",
            command=self.previous_page,
            font=("Arial", 9),
            state='disabled'
        )
        self.prev_button.pack(side='left', padx=2)
        
        self.next_button = tk.Button(
            nav_frame,
            text="След ▶",
            command=self.next_page,
            font=("Arial", 9)
        )
        self.next_button.pack(side='left', padx=2)
        
        # Переход к странице
        goto_frame = tk.Frame(pagination_container, bg='lightblue')
        goto_frame.pack(side='left', padx=10)
        
        tk.Label(goto_frame, text="Перейти к:", font=("Arial", 9), bg='lightblue').pack(side='left')
        
        self.page_entry = tk.Entry(goto_frame, width=5, font=("Arial", 9))
        self.page_entry.pack(side='left', padx=5)
        
        go_button = tk.Button(
            goto_frame,
            text="Перейти",
            command=self.go_to_page,
            font=("Arial", 8)
        )
        go_button.pack(side='left')
        
        # Настройки отображения
        rows_frame = tk.Frame(pagination_container, bg='lightblue')
        rows_frame.pack(side='left', padx=10)
        
        tk.Label(rows_frame, text="Строк на странице:", font=("Arial", 9), bg='lightblue').pack(side='left')
        
        self.rows_per_page_var = tk.StringVar(value="20")
        rows_combo = ttk.Combobox(rows_frame, textvariable=self.rows_per_page_var, width=8)
        rows_combo['values'] = ("10", "20", "50", "100")
        rows_combo.pack(side='left', padx=5)
        
        # Кнопка обновления
        refresh_frame = tk.Frame(pagination_container, bg='lightblue')
        refresh_frame.pack(side='right', padx=20)
        
        refresh_button = tk.Button(
            refresh_frame,
            text="🔄 Обновить",
            command=self.refresh_data,
            font=("Arial", 9),
            bg='#4CAF50',
            fg='white',
            padx=10,
            pady=5
        )
        refresh_button.pack()
    
    def populate_test_data(self):
        """Заполняет таблицу тестовыми данными"""
        test_data = [
            ("☐", "PROJ-123", "Исправить ошибку в аутентификации", "In Progress", "High", "Иван Петров", "2024-03-15", "Детали | PDF | JIRA"),
            ("☐", "PROJ-124", "Добавить новую функцию экспорта", "To Do", "Medium", "Мария Сидорова", "2024-03-14", "Детали | PDF | JIRA"),
            ("☐", "PROJ-125", "Обновить документацию API", "Done", "Low", "Алексей Смирнов", "2024-03-13", "Детали | PDF | JIRA"),
            ("☐", "PROJ-126", "Оптимизировать производительность", "In Progress", "Highest", "Елена Козлова", "2024-03-12", "Детали | PDF | JIRA"),
            ("☐", "PROJ-127", "Настроить CI/CD pipeline", "To Do", "High", "Дмитрий Волков", "2024-03-11", "Детали | PDF | JIRA"),
        ]
        
        for i, item in enumerate(test_data):
            task_id = self.tasks_tree.insert("", "end", values=item)
    
    def login_to_jira(self):
        """Обработчик входа в JIRA"""
        url = self.url_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not url or not email or not password:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return
        
        # Здесь будет реальная логика подключения к JIRA
        messagebox.showinfo("Успех", f"Подключение к JIRA успешно!\nURL: {url}\nEmail: {email}")
        
        # Переключаемся на вкладку с задачами
        self.notebook.select(1)
    
    def apply_filters(self):
        """Применяет выбранные фильтры"""
        status = self.status_var.get()
        priority = self.priority_var.get()
        assignee = self.assignee_entry.get().strip()
        search_text = self.search_entry.get().strip()
        
        # Здесь будет реальная логика фильтрации
        messagebox.showinfo("Фильтры", f"Применены фильтры:\nСтатус: {status}\nПриоритет: {priority}\nИсполнитель: {assignee}\nПоиск: {search_text}")
    
    def reset_filters(self):
        """Сбрасывает все фильтры"""
        self.status_var.set("Все")
        self.priority_var.set("Все")
        self.assignee_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        messagebox.showinfo("Фильтры", "Все фильтры сброшены")
    
    def previous_page(self):
        """Переход к предыдущей странице"""
        messagebox.showinfo("Пагинация", "Переход к предыдущей странице")
    
    def next_page(self):
        """Переход к следующей странице"""
        messagebox.showinfo("Пагинация", "Переход к следующей странице")
    
    def go_to_page(self):
        """Переход к указанной странице"""
        page = self.page_entry.get().strip()
        if page.isdigit():
            messagebox.showinfo("Пагинация", f"Переход к странице {page}")
        else:
            messagebox.showerror("Ошибка", "Введите корректный номер страницы")
    
    def refresh_data(self):
        """Обновление данных"""
        messagebox.showinfo("Обновление", "Данные обновлены")
    
    # Методы для работы с чекбоксами и действиями
    def toggle_all_selection(self):
        """Переключает выделение всех задач"""
        self.all_selected = not self.all_selected
        
        if self.all_selected:
            # Выделяем все
            for item in self.tasks_tree.get_children():
                self.selected_tasks.add(item)
                values = list(self.tasks_tree.item(item, 'values'))
                values[0] = "☑"  # Отмеченный чекбокс
                self.tasks_tree.item(item, values=values)
            self.tasks_tree.heading("Выбрать", text="☑ Все")
        else:
            # Снимаем выделение
            self.selected_tasks.clear()
            for item in self.tasks_tree.get_children():
                values = list(self.tasks_tree.item(item, 'values'))
                values[0] = "☐"  # Пустой чекбокс
                self.tasks_tree.item(item, values=values)
            self.tasks_tree.heading("Выбрать", text="☐ Все")
    
    def on_task_click(self, event):
        """Обрабатывает клик по задаче"""
        region = self.tasks_tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tasks_tree.identify_column(event.x)
            item = self.tasks_tree.identify_row(event.y)
            
            if item and column == '#1':  # Колонка чекбоксов
                self.toggle_task_selection(item)
            elif item and column == '#8':  # Колонка действий
                self.show_action_menu(event, item)
    
    def toggle_task_selection(self, item):
        """Переключает выделение одной задачи"""
        values = list(self.tasks_tree.item(item, 'values'))
        
        if item in self.selected_tasks:
            # Снимаем выделение
            self.selected_tasks.remove(item)
            values[0] = "☐"
        else:
            # Добавляем в выделенные
            self.selected_tasks.add(item)
            values[0] = "☑"
        
        self.tasks_tree.item(item, values=values)
        
        # Обновляем состояние главного чекбокса
        total_items = len(self.tasks_tree.get_children())
        selected_count = len(self.selected_tasks)
        
        if selected_count == 0:
            self.tasks_tree.heading("Выбрать", text="☐ Все")
            self.all_selected = False
        elif selected_count == total_items:
            self.tasks_tree.heading("Выбрать", text="☑ Все")
            self.all_selected = True
        else:
            self.tasks_tree.heading("Выбрать", text="☣ Все")
            self.all_selected = False
    
    def show_action_menu(self, event, item):
        """Показывает меню действий для задачи"""
        # Получаем данные задачи
        values = self.tasks_tree.item(item, 'values')
        task_id = values[1]
        
        # Создаем контекстное меню
        action_menu = tk.Menu(self.root, tearoff=0)
        action_menu.add_command(label="📝 Детали", command=lambda: self.show_task_details(item))
        action_menu.add_command(label="📚 PDF", command=lambda: self.export_task_pdf(item))
        action_menu.add_command(label="🔗 Открыть в JIRA", command=lambda: self.open_in_jira(item))
        
        try:
            action_menu.tk_popup(event.x_root, event.y_root)
        finally:
            action_menu.grab_release()
    
    def on_task_double_click(self, event):
        """Обрабатывает двойной клик по задаче"""
        item = self.tasks_tree.selection()[0] if self.tasks_tree.selection() else None
        if item:
            self.show_task_details(item)
    
    def show_task_details(self, item):
        """Показывает модальное окно с деталями задачи"""
        values = self.tasks_tree.item(item, 'values')
        
        # Создаем модальное окно
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Детали задачи {values[1]}")
        details_window.geometry("500x400")
        details_window.transient(self.root)
        details_window.grab_set()
        
        # Создаем форму с отключенными полями
        tk.Label(details_window, text="ID задачи:", font=("Arial", 10, "bold")).pack(anchor='w', padx=20, pady=(20, 5))
        id_entry = tk.Entry(details_window, font=("Arial", 10), state='disabled')
        id_entry.pack(fill='x', padx=20, pady=(0, 10))
        id_entry.config(state='normal')
        id_entry.insert(0, values[1])
        id_entry.config(state='disabled')
        
        tk.Label(details_window, text="Заголовок:", font=("Arial", 10, "bold")).pack(anchor='w', padx=20, pady=5)
        title_entry = tk.Entry(details_window, font=("Arial", 10), state='disabled')
        title_entry.pack(fill='x', padx=20, pady=(0, 10))
        title_entry.config(state='normal')
        title_entry.insert(0, values[2])
        title_entry.config(state='disabled')
        
        tk.Label(details_window, text="Статус:", font=("Arial", 10, "bold")).pack(anchor='w', padx=20, pady=5)
        status_entry = tk.Entry(details_window, font=("Arial", 10), state='disabled')
        status_entry.pack(fill='x', padx=20, pady=(0, 10))
        status_entry.config(state='normal')
        status_entry.insert(0, values[3])
        status_entry.config(state='disabled')
        
        tk.Label(details_window, text="Приоритет:", font=("Arial", 10, "bold")).pack(anchor='w', padx=20, pady=5)
        priority_entry = tk.Entry(details_window, font=("Arial", 10), state='disabled')
        priority_entry.pack(fill='x', padx=20, pady=(0, 10))
        priority_entry.config(state='normal')
        priority_entry.insert(0, values[4])
        priority_entry.config(state='disabled')
        
        tk.Label(details_window, text="Исполнитель:", font=("Arial", 10, "bold")).pack(anchor='w', padx=20, pady=5)
        assignee_entry = tk.Entry(details_window, font=("Arial", 10), state='disabled')
        assignee_entry.pack(fill='x', padx=20, pady=(0, 10))
        assignee_entry.config(state='normal')
        assignee_entry.insert(0, values[5])
        assignee_entry.config(state='disabled')
        
        tk.Label(details_window, text="Обновлено:", font=("Arial", 10, "bold")).pack(anchor='w', padx=20, pady=5)
        updated_entry = tk.Entry(details_window, font=("Arial", 10), state='disabled')
        updated_entry.pack(fill='x', padx=20, pady=(0, 20))
        updated_entry.config(state='normal')
        updated_entry.insert(0, values[6])
        updated_entry.config(state='disabled')
        
        # Кнопка закрытия
        tk.Button(
            details_window,
            text="Закрыть",
            command=details_window.destroy,
            font=("Arial", 12),
            bg='#95A5A6',
            fg='white',
            padx=20,
            pady=10
        ).pack(pady=20)
    
    def export_task_pdf(self, item):
        """Экспортирует задачу в PDF"""
        from tkinter import filedialog
        
        values = self.tasks_tree.item(item, 'values')
        task_id = values[1]
        
        # Открываем диалог сохранения
        filename = filedialog.asksaveasfilename(
            title=f"Сохранить PDF для {task_id}",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("Все файлы", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(f"PDF отчет для задачи {task_id}\n")
                    f.write(f"Заголовок: {values[2]}\n")
                    f.write(f"Статус: {values[3]}\n")
                    f.write(f"Приоритет: {values[4]}\n")
                    f.write(f"Исполнитель: {values[5]}\n")
                    f.write(f"Обновлено: {values[6]}\n")
                
                messagebox.showinfo("Успех", f"PDF сохранен: {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")
    
    def open_in_jira(self, item):
        """Открывает задачу в JIRA"""
        import webbrowser
        
        values = self.tasks_tree.item(item, 'values')
        task_id = values[1]
        
        # Получаем URL из поля входа (если заполнено)
        jira_url = getattr(self, 'url_entry', None)
        if jira_url and jira_url.get().strip():
            base_url = jira_url.get().strip().rstrip('/')
            full_url = f"{base_url}/browse/{task_id}"
        else:
            # Используем заглушку
            full_url = f"https://your-jira-instance.com/browse/{task_id}"
        
        try:
            webbrowser.open(full_url)
            messagebox.showinfo("Успех", f"Открываем задачу {task_id} в браузере")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка открытия браузера: {str(e)}")
    
    def bulk_export_pdf(self):
        """Массовый экспорт выбранных задач в PDF"""
        if not self.selected_tasks:
            messagebox.showwarning("Предупреждение", "Не выбрано ни одной задачи")
            return
        
        from tkinter import filedialog
        import os
        
        # Открываем диалог выбора папки
        folder = filedialog.askdirectory(
            title=f"Выберите папку для сохранения {len(self.selected_tasks)} PDF файлов"
        )
        
        if folder:
            exported_count = 0
            for item in self.selected_tasks:
                values = self.tasks_tree.item(item, 'values')
                task_id = values[1]
                filename = os.path.join(folder, f"task_{task_id}.pdf")
                
                try:
                    with open(filename, 'w') as f:
                        f.write(f"PDF отчет для задачи {task_id}\n")
                        f.write(f"Заголовок: {values[2]}\n")
                        f.write(f"Статус: {values[3]}\n")
                        f.write(f"Приоритет: {values[4]}\n")
                        f.write(f"Исполнитель: {values[5]}\n")
                        f.write(f"Обновлено: {values[6]}\n")
                    exported_count += 1
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка сохранения {task_id}: {str(e)}")
            
            messagebox.showinfo("Успех", f"Экспортировано {exported_count} из {len(self.selected_tasks)} задач")
    
    def clear_selection(self):
        """Снимает выделение со всех задач"""
        self.selected_tasks.clear()
        for item in self.tasks_tree.get_children():
            values = list(self.tasks_tree.item(item, 'values'))
            values[0] = "☐"
            self.tasks_tree.item(item, values=values)
        self.tasks_tree.heading("Выбрать", text="☐ Все")
        self.all_selected = False

def main():
    # Создаем главное окно
    root = tk.Tk()
    
    # Создаем приложение
    app = JiraExportApp(root)
    
    # Запускаем главный цикл
    root.mainloop()

if __name__ == "__main__":
    main()