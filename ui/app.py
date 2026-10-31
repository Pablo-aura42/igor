# Главное окно калькулятора: меню, темы, горячие клавиши

import tkinter as tk
import webbrowser
from tkinter import messagebox

import customtkinter as ctk

from config import (
    APP_TITLE, APP_WIDTH, APP_HEIGHT, PADDING_OUTER, OPERATORS, DEFAULT_THEME,
)
from core.calculator import CalculatorEngine
from core.themes import ThemeManager
from ui.display import Display
from ui.button_panel import ButtonPanel
from ui.menu_bar import MenuBar, CommandItem, SeparatorItem, RadioItem

GITHUB_URL = "https://github.com/Pablo-aura42/igor"


class CalculatorApp(ctk.CTk):
    """Корневое окно приложения."""

    def __init__(self):
        super().__init__()

        self.engine = CalculatorEngine()
        self.theme_manager = ThemeManager(DEFAULT_THEME)

        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode(self.theme_manager.current["mode"])

        self._setup_window()
        self._build_menu()
        self._build_widgets()
        self._apply_theme(self.theme_manager.current_name)
        self._setup_hotkeys()
        self._refresh_display()

    # ---------------- Окно ----------------
    def _setup_window(self):
        self.title(APP_TITLE)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.resizable(False, False)

    # ---------------- Меню ----------------
    def _build_menu(self):
        self._theme_var = tk.StringVar(value=self.theme_manager.current_name)
        self._mode_var = tk.StringVar(value="normal")

        self.menu_bar = MenuBar(self, self.theme_manager.current)
        self.menu_bar.pack(fill="x")

        # Калькулятор
        self.menu_bar.add_menu("Калькулятор", [
            CommandItem("Очистить", lambda: self.handle_button("C"), "Ctrl+L"),
            SeparatorItem(),
            CommandItem("Выход", self.destroy, "Ctrl+Q"),
        ])

        # Режим
        self.menu_bar.add_menu("Режим", [
            RadioItem("Обычный", "normal", self._mode_var, self._set_mode),
            RadioItem("Научный", "scientific", self._mode_var, self._set_mode),
        ])

        # Вид — сразу список тем (без подменю, чтобы не усложнять)
        theme_items = [
            RadioItem(name, name, self._theme_var, self._apply_theme)
            for name in self.theme_manager.names
        ]
        self.menu_bar.add_menu("Вид", theme_items)

        # Справка
        self.menu_bar.add_menu("Справка", [
            CommandItem("О программе", self._show_about),
            CommandItem("GitHub", lambda: webbrowser.open(GITHUB_URL)),
        ])

    def _set_mode(self, mode):
        self._mode_var.set(mode)
        # TODO: реальное переключение режима (научный пока заглушка)

    # ---------------- Виджеты ----------------
    def _build_widgets(self):
        self.display = Display(self)
        self.display.pack(
            padx=PADDING_OUTER,
            pady=(PADDING_OUTER, 10),
            fill="x",
        )

        self.panel = ButtonPanel(
            self,
            on_press=self.handle_button,
            theme=self.theme_manager.current,
        )
        self.panel.pack(
            padx=PADDING_OUTER,
            pady=PADDING_OUTER,
            fill="both",
            expand=True,
        )

    # ---------------- Тема ----------------
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

    # ---------------- Горячие клавиши ----------------
    def _setup_hotkeys(self):
        self.bind("<Key>", self._on_key)
        self.display.bind("<Key>", self._on_key)
        self.bind("<Control-l>", lambda e: (self.handle_button("C"), "break")[1])
        self.bind("<Control-q>", lambda e: (self.destroy(), "break")[1])

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
        if char == "=":
            self.handle_button("="); return "break"

        if keysym in ("Return", "KP_Enter"):
            self.handle_button("="); return "break"
        if keysym == "BackSpace":
            self.handle_button("⌫"); return "break"
        if keysym in ("Escape", "Delete"):
            self.handle_button("C"); return "break"

    # ---------------- Справка ----------------
    def _show_about(self):
        messagebox.showinfo(
            "О программе",
            "igor — маленький калькулятор\n"
            "Версия 0.3\n\n"
            "Python + CustomTkinter\n"
            f"Тема: {self.theme_manager.current_name}",
        )

    # ---------------- Дисплей ----------------
    def _refresh_display(self):
        self.display.show(
            self.engine.get_display_text(),
            error=self.engine.is_error,
        )

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
