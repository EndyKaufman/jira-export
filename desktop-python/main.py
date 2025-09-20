import tkinter as tk
from tkinter import messagebox

class HelloWorldApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Привет Мир - Десктопное приложение")
        self.root.geometry("400x300")
        self.root.resizable(True, True)
        
        # Создаем главный фрейм
        main_frame = tk.Frame(root, bg='lightblue', padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Заголовок
        title_label = tk.Label(
            main_frame, 
            text="Добро пожаловать!", 
            font=("Arial", 16, "bold"),
            bg='lightblue',
            fg='darkblue'
        )
        title_label.pack(pady=20)
        
        # Кнопка для показа уведомления
        hello_button = tk.Button(
            main_frame,
            text="Нажми меня!",
            command=self.show_hello_notification,
            font=("Arial", 12),
            bg='white',
            fg='black',
            padx=20,
            pady=10,
            relief='raised',
            bd=3
        )
        hello_button.pack(pady=20)
        
        # Информационная метка
        info_label = tk.Label(
            main_frame,
            text="Нажмите кнопку для получения уведомления",
            font=("Arial", 10),
            bg='lightblue',
            fg='gray'
        )
        info_label.pack(pady=10)
    
    def show_hello_notification(self):
        """Показывает уведомление 'Привет мир'"""
        messagebox.showinfo("Уведомление", "Привет мир!")

def main():
    # Создаем главное окно
    root = tk.Tk()
    
    # Создаем приложение
    app = HelloWorldApp(root)
    
    # Запускаем главный цикл
    root.mainloop()

if __name__ == "__main__":
    main()