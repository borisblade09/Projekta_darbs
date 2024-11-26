from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit
)
import sqlite3
import smtplib


class EmailApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройка электронной почты")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()
        self.setup_database()

    def init_ui(self):
        layout = QVBoxLayout()

        # Поле ввода email
        self.label_email = QLabel("Введите ваш адрес электронной почты:")
        layout.addWidget(self.label_email)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@mail.com")
        layout.addWidget(self.email_input)

        # Кнопка тестирования SMTP
        self.test_button = QPushButton("Проверить соединение с SMTP")
        self.test_button.clicked.connect(self.test_smtp_connection)
        layout.addWidget(self.test_button)

        # Кнопка сохранения email
        self.save_button = QPushButton("Сохранить email")
        self.save_button.clicked.connect(self.save_email)
        layout.addWidget(self.save_button)

        # Поле вывода сообщений
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.setLayout(layout)

    def setup_database(self):
        """Создание базы данных, если её нет."""
        conn = sqlite3.connect("emails.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def test_smtp_connection(self):
        """Проверка соединения с SMTP сервером."""
        email = self.email_input.text()
        try:
            # Проверяем базовые ошибки
            if "@" not in email or "." not in email:
                raise ValueError("Неверный формат email!")
            # Пробуем подключиться к SMTP (например, Gmail)
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.quit()
            self.log.append("Успешное подключение к SMTP серверу!")
        except Exception as e:
            self.log.append(f"Ошибка подключения к SMTP: {e}")

    def save_email(self):
        """Сохранение email в базу данных."""
        email = self.email_input.text()
        if "@" in email and "." in email:
            try:
                conn = sqlite3.connect("emails.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO emails (email) VALUES (?)", (email,))
                conn.commit()
                conn.close()
                self.log.append(f"Email сохранен: {email}")
            except Exception as e:
                self.log.append(f"Ошибка при сохранении email: {e}")
        else:
            self.log.append("Введите корректный email!")


if __name__ == "__main__":
    app = QApplication([])
    window = EmailApp()
    window.show()
    app.exec_()
