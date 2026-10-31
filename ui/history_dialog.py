# Окно с историей вычислений

import customtkinter as ctk


class HistoryDialog(ctk.CTkToplevel):
    """Модальное окно истории. По клику на запись отдаёт результат наверх."""

    def __init__(self, parent, settings, theme, on_use):
        super().__init__(parent)
        self.settings = settings
        self._theme = theme
        self._on_use = on_use

        self.title("История")
        self.geometry("300x420")
        self.resizable(False, True)
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
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        w, h = 300, 420
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ---------------- Содержимое ----------------
    def _build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(12, 6))

        ctk.CTkLabel(
            header, text="История",
            font=("Segoe UI", 16, "bold"),
            text_color=self._theme["display_fg"],
        ).pack(side="left")

        ctk.CTkButton(
            header, text="Очистить", width=80, height=26,
            fg_color=self._theme["func_bg"],
            hover_color=self._theme["func_hover"],
            text_color=self._theme["func_fg"],
            font=("Segoe UI", 12),
            command=self._clear,
        ).pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=self._theme["frame_bg"],
            corner_radius=8,
        )
        self.scroll.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self._render()

    # ---------------- Отрисовка записей ----------------
    def _render(self):
        for child in self.scroll.winfo_children():
            child.destroy()

        entries = list(self.settings.get_history())
        entries.reverse()   # свежие сверху

        if not entries:
            ctk.CTkLabel(
                self.scroll, text="Пусто",
                font=("Segoe UI", 12),
                text_color=self._theme["func_fg"],
            ).pack(pady=20)
            return

        for entry in entries:
            self._add_entry(entry)

    def _add_entry(self, entry):
        frame = ctk.CTkFrame(
            self.scroll,
            fg_color=self._theme["menu_dropdown_bg"],
            corner_radius=6,
        )
        frame.pack(fill="x", pady=2, padx=2)

        expr = ctk.CTkLabel(
            frame, text=entry["expr"],
            font=("Segoe UI", 11),
            text_color=self._theme["func_fg"],
            anchor="w",
        )
        expr.pack(fill="x", padx=8, pady=(6, 0))

        bottom = ctk.CTkFrame(frame, fg_color="transparent")
        bottom.pack(fill="x", padx=8, pady=(0, 6))

        res = ctk.CTkLabel(
            bottom, text="= " + entry["result"],
            font=("Segoe UI", 13, "bold"),
            text_color=self._theme["op_bg"],
            anchor="w",
        )
        res.pack(side="left")

        ctk.CTkLabel(
            bottom, text=entry.get("time", ""),
            font=("Segoe UI", 10),
            text_color=self._theme["func_hover"],
        ).pack(side="right")

        for w in (frame, expr, res, bottom):
            w.bind("<Button-1>", lambda e, r=entry["result"]: self._use(r))

    # ---------------- Действия ----------------
    def _use(self, result):
        self._on_use(result)
        self.destroy()

    def _clear(self):
        self.settings.clear_history()
        self._render()
