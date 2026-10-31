# Главное окно калькулятора: связывает движок и виджеты

import customtkinter as ctk

from config import APP_TITLE, APP_WIDTH, APP_HEIGHT, PADDING_OUTER, OPERATORS
from core.calculator import CalculatorEngine
from ui.display import Display
from ui.button_panel import ButtonPanel


class CalculatorApp(ctk.CTk):
    """Корневое окно приложения."""

    def __init__(self):
        super().__init__()

        # Движок вычислений (вся логика живёт там)
        self.engine = CalculatorEngine()

        self._setup_window()
        self._build_widgets()
        self._refresh_display()

    # ---------------- Настройка окна ----------------
    def _setup_window(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title(APP_TITLE)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.resizable(False, False)

    # ---------------- Виджеты ----------------
    def _build_widgets(self):
        # Дисплей
        self.display = Display(self)
        self.display.pack(
            padx=PADDING_OUTER,
            pady=(PADDING_OUTER, 10),
            fill="x",
        )

        # Панель кнопок
        self.panel = ButtonPanel(self, on_press=self.handle_button)
        self.panel.pack(
            padx=PADDING_OUTER,
            pady=PADDING_OUTER,
            fill="both",
            expand=True,
        )

    # ---------------- Обновление дисплея ----------------
    def _refresh_display(self):
        self.display.show(
            self.engine.get_display_text(),
            error=self.engine.is_error,
        )

    # ---------------- Обработка нажатий ----------------
    def handle_button(self, value):
        if value == "C":
            self.engine.reset()
        elif value == "⌫":
            self.engine.backspace()
        elif value.isdigit() or value == ".":
            self.engine.add_digit(value)
        elif value in OPERATORS:
            self.engine.set_operator(value)
        elif value == "=":
            self.engine.calculate()
        elif value == "±":
            self.engine.toggle_sign()
        elif value == "%":
            self.engine.apply_percent()

        self._refresh_display()
