# Главное окно: меню, темы, режимы, история, горячие клавиши

import tkinter as tk
import webbrowser

import customtkinter as ctk

from config import (
    APP_TITLE, APP_WIDTH, APP_HEIGHT, PADDING_OUTER,
    BINARY_OPERATORS, UNARY_OPERATORS, CONSTANTS,
    MODES, DEFAULT_THEME, DEFAULT_MODE,
)
from core.calculator import CalculatorEngine
from core.settings import Settings
from core.themes import ThemeManager
from ui.display import Display
from ui.button_panel import ButtonPanel
from ui.menu_bar import MenuBar, CommandItem, SeparatorItem, RadioItem
from ui.history_dialog import HistoryDialog
from ui.about_dialog import AboutDialog

GITHUB_URL = "https://github.com/Pablo-aura42/igor"


class CalculatorApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.engine = CalculatorEngine()
        self.settings = Settings()
        self.theme_manager = ThemeManager(
            self.settings.get("theme", DEFAULT_THEME)
        )

        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode(self.theme_manager.current["mode"])

        self._setup_window()
        self._build_menu()
        self._build_widgets()
        self._apply_theme(self.theme_manager.current_name)
        self._apply_mode(self.settings.get("mode", DEFAULT_MODE))
        self._setup_hotkeys()
        self._refresh_display()

        # Сохраняем при закрытии
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---------------- Окно ----------------
    def _setup_window(self):
        self.title(APP_TITLE)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.resizable(False, False)

    # ---------------- Меню ----------------
    def _build_menu(self):
        self._theme_var = tk.StringVar(value=self.theme_manager.current_name)
        self._mode_var = tk.StringVar(value=self.settings.get("mode", DEFAULT_MODE))

        self.menu_bar = MenuBar(self, self.theme_manager.current)
        self.menu_bar.pack(fill="x")

        # Калькулятор
        self.menu_bar.add_menu("Калькулятор", [
            CommandItem("История", self._open_history, "Ctrl+H"),
            SeparatorItem(),
            CommandItem("Очистить", lambda: self.handle_button("C"), "Ctrl+L"),
            CommandItem("Выход", self._on_close, "Ctrl+Q"),
        ])

        # Режим
        mode_items = [
            RadioItem(data["title"], key, self._mode_var,
                      lambda m, k=key: self._apply_mode(k))
            for key, data in MODES.items()
        ]
        self.menu_bar.add_menu("Режим", mode_items)

        # Вид — темы
        theme_items = [
            RadioItem(name, name, self._theme_var, self._apply_theme)
            for name in self.theme_manager.names
        ]
        self.menu_bar.add_menu("Вид", theme_items)

        # Справка
        self.menu_bar.add_menu("Справка", [
            CommandItem("О программе", self._open_about),
            CommandItem("GitHub", lambda: webbrowser.open(GITHUB_URL)),
        ])

    # ---------------- Виджеты ----------------
    def _build_widgets(self):
        self.display = Display(self)
        self.display.pack(
            padx=PADDING_OUTER, pady=(PADDING_OUTER, 10), fill="x",
        )

        mode_key = self.settings.get("mode", DEFAULT_MODE)
        mode = MODES.get(mode_key, MODES[DEFAULT_MODE])

        self.panel = ButtonPanel(
            self,
            on_press=self.handle_button,
            theme=self.theme_manager.current,
            layout=mode["layout"],
            columns=mode["columns"],
        )
        self.panel.pack(
            padx=PADDING_OUTER, pady=PADDING_OUTER,
            fill="both", expand=True,
        )

    # ---------------- Применение темы ----------------
    def _apply_theme(self, name):
        self.theme_manager.set(name)
        theme = self.theme_manager.current

        ctk.set_appearance_mode(theme["mode"])
        self.configure(fg_color=theme["bg"])

        if hasattr(self, "menu_bar"):
            self.menu_bar.apply_theme(theme)
        if hasattr(self, "display"):
            self.display.apply_theme(theme)
        if hasattr(self, "panel"):
            self.panel.apply_theme(theme)

        if hasattr(self, "_theme_var"):
            self._theme_var.set(name)
        self.settings.set("theme", name)

    # ---------------- Применение режима ----------------
    def _apply_mode(self, mode_key):
        if mode_key not in MODES:
            return
        mode = MODES[mode_key]

        if hasattr(self, "panel"):
            self.panel.set_layout(mode["layout"], mode["columns"])

        if hasattr(self, "_mode_var"):
            self._mode_var.set(mode_key)

        self.settings.set("mode", mode_key)

    # ---------------- Диалоги ----------------
    def _open_history(self):
        HistoryDialog(
            parent=self,
            settings=self.settings,
            theme=self.theme_manager.current,
            on_use=self._use_history_value,
        )

    def _use_history_value(self, value):
        self.engine.load_value(value)
        self._refresh_display()

    def _open_about(self):
        AboutDialog(self, self.theme_manager.current, version="0.4")

    # ---------------- Закрытие ----------------
    def _on_close(self):
        self.settings.save()
        self.destroy()

    # ---------------- Горячие клавиши ----------------
    def _setup_hotkeys(self):
        self.bind("<Key>", self._on_key)
        self.display.bind("<Key>", self._on_key)
        self.bind("<Control-l>", lambda e: (self.handle_button("C"), "break")[1])
        self.bind("<Control-q>", lambda e: (self._on_close(), "break")[1])
        self.bind("<Control-h>", lambda e: (self._open_history(), "break")[1])

    def _on_key(self, event):
        char, keysym = event.char, event.keysym

        if char.isdigit():
            self.handle_button(char); return "break"
        if char in (".", ","):
            self.handle_button("."); return "break"
        if char == "+":
            self.handle_button("+"); return "break"
        if char == "-":
            self.handle_button("−"); return "break"
        if char == "*":
            self.handle_button("×"); return "break"
        if char == "/":
            self.handle_button("÷"); return "break"
        if char == "%":
            self.handle_button("%"); return "break"
        if char == "^":
            self.handle_button("xʸ"); return "break"
        if char == "=":
            self.handle_button("="); return "break"

        if keysym in ("Return", "KP_Enter"):
            self.handle_button("="); return "break"
        if keysym == "BackSpace":
            self.handle_button("⌫"); return "break"
        if keysym in ("Escape", "Delete"):
            self.handle_button("C"); return "break"

    # ---------------- Дисплей ----------------
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
        elif value in BINARY_OPERATORS:
            self.engine.set_operator(value)
        elif value in UNARY_OPERATORS:
            self.engine.apply_unary(value)
        elif value in CONSTANTS:
            self.engine.insert_constant(value)
        elif value == "=":
            result = self.engine.calculate()
            if result:
                expression, formatted = result
                self.settings.add_history(expression, formatted)
        elif value == "±":
            self.engine.toggle_sign()
        elif value == "%":
            self.engine.apply_percent()

        self._refresh_display()
