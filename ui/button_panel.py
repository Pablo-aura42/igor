# Панель с кнопками калькулятора

import customtkinter as ctk

from config import (
    BUTTONS_LAYOUT,
    BUTTON_FONT,
    BUTTON_HEIGHT,
    BUTTON_WIDTH,
    CORNER_RADIUS,
    PADDING_INNER,
)

# Количество колонок в сетке кнопок
COLUMNS = 4


class ButtonPanel(ctk.CTkFrame):
    """Сетка кнопок. Все нажатия пробрасывает через колбэк on_press."""

    def __init__(self, master, on_press):
        super().__init__(master, corner_radius=CORNER_RADIUS)
        self.on_press = on_press
        self._build()

    # ---------------- Построение сетки ----------------
    def _build(self):
        # Настраиваем все колонки один раз
        for col in range(COLUMNS):
            self.columnconfigure(col, weight=1)

        for row_index, row in enumerate(BUTTONS_LAYOUT):
            self.rowconfigure(row_index, weight=1)

            # Строка из одной кнопки — растягиваем её на всю ширину
            if len(row) == 1:
                self._add_button(row[0], row_index, 0, span=COLUMNS)
                continue

            col_index = 0
            for text in row:
                # Кнопка "0" занимает две колонки
                if text == "0":
                    self._add_button(text, row_index, col_index, span=2)
                    col_index += 2
                else:
                    self._add_button(text, row_index, col_index)
                    col_index += 1

    # ---------------- Создание одной кнопки ----------------
    def _add_button(self, text, row, column, span=1):
        button = ctk.CTkButton(
            self,
            text=text,
            font=BUTTON_FONT,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            command=lambda t=text: self.on_press(t),
        )
        button.grid(
            row=row,
            column=column,
            columnspan=span,
            padx=PADDING_INNER,
            pady=PADDING_INNER,
            sticky="nsew",
        )
