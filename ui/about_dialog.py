# Окно «О программе» с кнопкой удаления конфига

import customtkinter as ctk

from core.settings import Settings


class AboutDialog(ctk.CTkToplevel):
    """Модальное окно с информацией о приложении и удалением конфига."""

    def __init__(self, parent, theme, version="0.4"):
        super().__init__(parent)
        self._theme = theme
        self._version = version

        self.title("О программе")
        self.geometry("340x260")
        self.resizable(False, False)
        self.configure(fg_color=theme["bg"])
        self.transient(parent)
        self._center_on(parent)

        self._build()

        # Отложенный grab_set: окно должно успеть стать viewable
        self.after(10, self._grab)
        # Escape закрывает окно
        self.bind("<Escape>", lambda e: self.destroy())

    # ---------------- Захват ввода ----------------
    def _grab(self):
        """Безопасный grab_set — только когда окно уже видимо."""
        try:
            self.grab_set()
            self.focus_set()
        except Exception:
            pass

    # ---------------- Позиционирование ----------------
    def _center_on(self, parent):
        parent.update_idletasks()
        px, py = parent.winfo_rootx(), parent.winfo_rooty()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        w, h = 340, 260
        x, y = px + (pw - w) // 2, py + (ph - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ---------------- Содержимое ----------------
    def _build(self):
        t = self._theme
        pad = 16

        ctk.CTkLabel(
            self, text="igor",
            font=("Segoe UI", 24, "bold"),
            text_color=t["op_bg"],
        ).pack(pady=(pad, 0))

        ctk.CTkLabel(
            self, text=f"версия {self._version}",
            font=("Segoe UI", 11),
            text_color=t["func_fg"],
        ).pack()

        ctk.CTkLabel(
            self,
            text="Маленький калькулятор на Python + CustomTkinter",
            font=("Segoe UI", 12),
            text_color=t["display_fg"],
            wraplength=300,
        ).pack(pady=(10, 4))

        ctk.CTkLabel(
            self,
            text=f"Конфиг: {Settings.config_path()}",
            font=("Segoe UI", 10),
            text_color=t["func_hover"],
            wraplength=300,
        ).pack(pady=(0, 10))

        # Кнопки
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(0, pad))

        ctk.CTkButton(
            btn_row, text="Удалить конфиг",
            width=140, height=32,
            fg_color=t["display_error"],
            hover_color=t["func_bg"],
            text_color=t["bg"],
            font=("Segoe UI", 12),
            command=self._delete_config,
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            btn_row, text="Закрыть",
            width=100, height=32,
            fg_color=t["func_bg"],
            hover_color=t["func_hover"],
            text_color=t["func_fg"],
            font=("Segoe UI", 12),
            command=self.destroy,
        ).pack(side="left", padx=4)

        self._status = ctk.CTkLabel(
            self, text="",
            font=("Segoe UI", 11),
            text_color=t["equal_bg"],
        )
        self._status.pack()

    # ---------------- Удаление конфига ----------------
    def _delete_config(self):
        deleted = Settings.delete_config()
        if deleted:
            self._status.configure(
                text="Конфиг удалён. Изменения вступят в силу при следующем запуске.",
                text_color=self._theme["equal_bg"],
            )
        else:
            self._status.configure(
                text="Конфиг не найден.",
                text_color=self._theme["display_error"],
            )
