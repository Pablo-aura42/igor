# Кастомная панель меню, стилизованная под тему приложения

import tkinter.font as tkfont

import customtkinter as ctk


# ---------------- Модель пунктов меню ----------------
class CommandItem:
    """Пункт меню-команда."""
    def __init__(self, text, command, accelerator=None):
        self.text = text
        self.command = command
        self.accelerator = accelerator


class SeparatorItem:
    """Разделитель меню."""
    pass


class RadioItem:
    """Пункт меню с галочкой (выбор из набора)."""
    def __init__(self, text, value, variable, command=None):
        self.text = text
        self.value = value
        self.variable = variable
        self.command = command


# ---------------- Сама панель ----------------
class MenuBar(ctk.CTkFrame):
    """Стилизованная панель меню с выпадающими списками."""

    FONT_FAMILY = "Segoe UI"
    FONT_SIZE = 12
    BUTTON_HEIGHT = 26
    ITEM_HEIGHT = 28

    def __init__(self, master, theme):
        super().__init__(
            master,
            height=32,
            corner_radius=0,
            fg_color=theme["menu_bar_bg"],
        )
        self._theme = theme
        self._buttons = []              # [(button, label, items)]
        self._active_label = None       # какое меню сейчас открыто
        self._opened_by_hover = False   # открыто ли оно «ховером», а не кликом
        self._dropdown = None
        self.pack_propagate(False)

        # Шрифт для измерения ширины текста
        self._measure_font = tkfont.Font(
            family=self.FONT_FAMILY, size=self.FONT_SIZE
        )

        # Клик вне меню — закрыть; Escape — тоже закрыть
        self.winfo_toplevel().bind("<Button-1>", self._on_main_click, add="+")
        self.winfo_toplevel().bind("<Escape>", self._on_escape, add="+")

    # ---------------- Публичный API ----------------
    def add_menu(self, label, items):
        """Добавить меню. Ширина кнопки — по тексту, а не фиксированная."""
        width = self._measure_font.measure(label) + 24  # 12px отступ с каждой стороны

        btn = ctk.CTkButton(
            self,
            text=label,
            width=width,
            height=self.BUTTON_HEIGHT,
            corner_radius=4,
            fg_color="transparent",
            hover_color=self._theme["menu_button_hover"],
            text_color=self._theme["menu_button_fg"],
            font=(self.FONT_FAMILY, self.FONT_SIZE),
            command=lambda l=label, i=items: self._toggle(l, i),
        )
        btn.pack(side="left", padx=(4, 0), pady=3)

        # ⚡ Ключевая строка: ховер переключает открытое меню
        btn.bind(
            "<Enter>",
            lambda e, l=label, i=items: self._on_menu_hover(l, i),
        )

        self._buttons.append((btn, label, items))
        return btn

    def apply_theme(self, theme):
        self._theme = theme
        self.configure(fg_color=theme["menu_bar_bg"])
        for btn, _, _ in self._buttons:
            btn.configure(
                hover_color=theme["menu_button_hover"],
                text_color=theme["menu_button_fg"],
            )
        self._close_dropdown()

    # ---------------- Открытие / закрытие ----------------
    def _toggle(self, label, items):
        """Клик по кнопке меню."""
        if self._active_label == label:
            # Меню уже открыто на этой кнопке.
            # Если оно открылось ховером — клик его «подтверждает», не закрывая.
            # Если открылось кликом — обычный toggle: закрываем.
            if self._opened_by_hover:
                self._opened_by_hover = False
                return
            self._close_dropdown()
            return
        self._open_dropdown(label, items, by_hover=False)

    def _on_menu_hover(self, label, items):
        """Наведение на другую кнопку меню при открытом дропдауне."""
        if self._active_label is None:
            return                      # ничего не открыто — ховер не реагирует
        if self._active_label == label:
            return                      # уже открыто это меню — не трогаем
        self._open_dropdown(label, items, by_hover=True)

    def _open_dropdown(self, label, items, by_hover=False):
        self._close_dropdown()

        btn = next((b for b, lbl, _ in self._buttons if lbl == label), None)
        if not btn:
            return

        self._active_label = label
        self._opened_by_hover = by_hover

        x = self.winfo_x() + btn.winfo_x()
        y = self.winfo_y() + self.winfo_height()

        parent = self.winfo_toplevel()
        drop = ctk.CTkFrame(
            parent,
            fg_color=self._theme["menu_dropdown_bg"],
            corner_radius=8,
            border_width=1,
            border_color=self._theme["menu_dropdown_border"],
        )

        for item in items:
            self._add_item(drop, item)

        drop.place(x=x, y=y)
        drop.lift()
        self._dropdown = drop

        # Не вылезаем за правый край окна
        drop.update_idletasks()
        w = drop.winfo_width()
        if x + w > parent.winfo_width():
            drop.place(x=max(0, parent.winfo_width() - w - 4), y=y)

    def _close_dropdown(self):
        if self._dropdown:
            try:
                self._dropdown.destroy()
            except Exception:
                pass
            self._dropdown = None
        self._active_label = None
        self._opened_by_hover = False

    # ---------------- Отрисовка пунктов ----------------
    def _add_item(self, drop, item):
        if isinstance(item, SeparatorItem):
            sep = ctk.CTkFrame(
                drop, height=1,
                fg_color=self._theme["menu_dropdown_border"],
            )
            sep.pack(fill="x", padx=6, pady=4)
            return

        if isinstance(item, CommandItem):
            text = item.text
            if item.accelerator:
                text = f"{item.text}    {item.accelerator}"
            btn = ctk.CTkButton(
                drop,
                text=text,
                anchor="w",
                fg_color="transparent",
                hover_color=self._theme["menu_item_hover"],
                text_color=self._theme["menu_item_fg"],
                font=(self.FONT_FAMILY, self.FONT_SIZE),
                corner_radius=4,
                height=self.ITEM_HEIGHT,
                command=lambda c=item.command: self._run(c),
            )
            # fill="x" — классическое поведение меню:
            # все пункты выровнены по ширине самого длинного
            btn.pack(fill="x", padx=4, pady=1)
            return

        if isinstance(item, RadioItem):
            prefix = "✓  " if item.variable.get() == item.value else "    "
            btn = ctk.CTkButton(
                drop,
                text=prefix + item.text,
                anchor="w",
                fg_color="transparent",
                hover_color=self._theme["menu_item_hover"],
                text_color=self._theme["menu_item_fg"],
                font=(self.FONT_FAMILY, self.FONT_SIZE),
                corner_radius=4,
                height=self.ITEM_HEIGHT,
                command=lambda it=item: self._run_radio(it),
            )
            btn.pack(fill="x", padx=4, pady=1)

    # ---------------- Действия ----------------
    def _run(self, command):
        self._close_dropdown()
        if command:
            command()

    def _run_radio(self, item):
        item.variable.set(item.value)
        self._close_dropdown()
        if item.command:
            item.command(item.value)

    # ---------------- События окна ----------------
    def _on_main_click(self, event):
        if not self._dropdown:
            return
        if self._widget_in(event.widget, self._dropdown):
            return
        if self._widget_in(event.widget, self):
            return
        self._close_dropdown()

    def _on_escape(self, event):
        if self._dropdown:
            self._close_dropdown()
            return "break"

    @staticmethod
    def _widget_in(widget, container):
        while widget is not None:
            if widget == container:
                return True
            widget = getattr(widget, "master", None)
        return False
