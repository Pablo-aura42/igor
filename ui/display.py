# Виджет дисплея калькулятора

import customtkinter as ctk

from config import DISPLAY_FONT, DISPLAY_HEIGHT, CORNER_RADIUS

# Цвета текста в зависимости от состояния
NORMAL_TEXT_COLOR = ("#000000", "#dce4ee")   # (светлая тема, тёмная тема)
ERROR_TEXT_COLOR = ("#cc0000", "#ff5555")


class Display(ctk.CTkEntry):
    """Поле ввода, работающее как дисплей (только для чтения)."""

    def __init__(self, master):
        super().__init__(
            master,
            height=DISPLAY_HEIGHT,
            font=DISPLAY_FONT,
            justify="right",
            corner_radius=CORNER_RADIUS,
        )

    def show(self, text, error=False):
        """Полностью заменить содержимое дисплея."""
        self.delete(0, "end")
        self.insert(0, text)
        # Красный цвет при ошибке, обычный — в остальных случаях
        self.configure(text_color=ERROR_TEXT_COLOR if error else NORMAL_TEXT_COLOR)
