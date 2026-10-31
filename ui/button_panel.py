# Панель с кнопками калькулятора

import customtkinter as ctk

from config import (
    BUTTON_FONT,
    BUTTON_HEIGHT,
    BUTTON_WIDTH,
    CORNER_RADIUS,
    PADDING_INNER,
    BINARY_OPERATORS,
    UNARY_OPERATORS,
)

FUNC_BUTTONS = {"C", "⌫", "±", "%", "+%", "-%"}


class ButtonPanel(ctk.CTkFrame):
    """Сетка кнопок. Пересобирается при смене режима."""

    def __init__(self, master, on_press, theme, layout, columns):
        super().__init__(master, corner_radius=CORNER_RADIUS)
        self.on_press = on_press
        self._theme = theme
        self._layout = layout
        self._columns = columns
        self._buttons = []
        self._build()

    # ---------------- Пересборка ----------------
    def set_layout(self, layout, columns):
        for child in self.winfo_children():
            child.destroy()
        self._buttons.clear()
        self._layout = layout
        self._columns = columns
        self._build()

    # ---------------- Классификация ----------------
    @staticmethod
    def _classify(text):
        if text in FUNC_BUTTONS:
            return "func"
        if text == "=":
            return "equal"
        if text in BINARY_OPERATORS or text in UNARY_OPERATORS:
            return "op"
        return "digit"

    def _colors_for(self, category):
        t = self._theme
        if category == "func":
            return t["func_bg"], t["func_hover"], t["func_fg"]
        if category == "equal":
            return t["equal_bg"], t["equal_hover"], t["equal_fg"]
        if category == "op":
            return t["op_bg"], t["op_hover"], t["op_fg"]
        return t["btn_bg"], t["btn_hover"], t["btn_fg"]

    # ---------------- Построение ----------------
    def _build(self):
        self.configure(fg_color=self._theme["frame_bg"])

        for col in range(self._columns):
            self.columnconfigure(col, weight=1)

        for row_index, row in enumerate(self._layout):
            self.rowconfigure(row_index, weight=1)

            col_index = 0
            for text in row:
                if text == "⌫":
                    span = self._columns
                elif text == "0" and self._columns == 4:
                    span = 2
                else:
                    span = 1

                self._add_button(text, row_index, col_index, span=span)
                col_index += span

    def _add_button(self, text, row, column, span=1):
        category = self._classify(text)
        bg, hover, fg = self._colors_for(category)

        button = ctk.CTkButton(
            self,
            text=text,
            font=BUTTON_FONT,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color=bg,
            hover_color=hover,
            text_color=fg,
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
        self._buttons.append((button, category))

    # ---------------- Смена темы ----------------
    def apply_theme(self, theme):
        self._theme = theme
        self.configure(fg_color=theme["frame_bg"])
        for button, category in self._buttons:
            bg, hover, fg = self._colors_for(category)
            button.configure(fg_color=bg, hover_color=hover, text_color=fg)
