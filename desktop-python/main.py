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
        tk.Label(parent, text="Список задач JIRA", font=("Arial", 12, "bold"), bg='white').pack(pady=10)
        
        # Создаем Treeview для таблицы
        columns = ("ID", "Заголовок", "Статус", "Приоритет", "Исполнитель", "Обновлено")
        self.tasks_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        # Настраиваем заголовки столбцов
        self.tasks_tree.heading("ID", text="ID")
        self.tasks_tree.heading("Заголовок", text="Заголовок")
        self.tasks_tree.heading("Статус", text="Статус")
        self.tasks_tree.heading("Приоритет", text="Приоритет")
        self.tasks_tree.heading("Исполнитель", text="Исполнитель")
        self.tasks_tree.heading("Обновлено", text="Обновлено")
        
        # Настраиваем ширину столбцов
        self.tasks_tree.column("ID", width=80, minwidth=60)
        self.tasks_tree.column("Заголовок", width=250, minwidth=150)
        self.tasks_tree.column("Статус", width=100, minwidth=80)
        self.tasks_tree.column("Приоритет", width=80, minwidth=60)
        self.tasks_tree.column("Исполнитель", width=120, minwidth=80)
        self.tasks_tree.column("Обновлено", width=100, minwidth=80)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем элементы
        self.tasks_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=(0, 10))
        scrollbar.pack(side='right', fill='y', pady=(0, 10))
        
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
            ("PROJ-123", "Исправить ошибку в аутентификации", "In Progress", "High", "Иван Петров", "2024-03-15"),
            ("PROJ-124", "Добавить новую функцию экспорта", "To Do", "Medium", "Мария Сидорова", "2024-03-14"),
            ("PROJ-125", "Обновить документацию API", "Done", "Low", "Алексей Смирнов", "2024-03-13"),
            ("PROJ-126", "Оптимизировать производительность", "In Progress", "Highest", "Елена Козлова", "2024-03-12"),
            ("PROJ-127", "Настроить CI/CD pipeline", "To Do", "High", "Дмитрий Волков", "2024-03-11"),
        ]
        
        for item in test_data:
            self.tasks_tree.insert("", "end", values=item)
    
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

def main():
    # Создаем главное окно
    root = tk.Tk()
    
    # Создаем приложение
    app = JiraExportApp(root)
    
    # Запускаем главный цикл
    root.mainloop()

if __name__ == "__main__":
    main()