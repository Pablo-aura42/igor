# Виджет дисплея калькулятора

import customtkinter as ctk

from config import DISPLAY_FONT, DISPLAY_HEIGHT, CORNER_RADIUS


class Display(ctk.CTkEntry):
    """Поле ввода, работающее как дисплей (только для чтения)."""

    def __init__(self, master):
        super().__init__(
            master,
            height=DISPLAY_HEIGHT,
            font=DISPLAY_FONT,
            justify="right",
            corner_radius=CORNER_RADIUS,
            border_width=0,
        )
        self._theme = None
        self._error = False

    # ---------------- Показ текста ----------------
    def show(self, text, error=False):
        self._error = error
        self.delete(0, "end")
        self.insert(0, text)
        self._refresh_color()

    # ---------------- Тема ----------------
    def apply_theme(self, theme):
        self._theme = theme
        self.configure(fg_color=theme["display_bg"])
        self._refresh_color()

    def _refresh_color(self):
        if not self._theme:
            return
        color = (
            self._theme["display_error"]
            if self._error
            else self._theme["display_fg"]
        )
        self.configure(text_color=color)
