# Сохранение настроек в ~/.config/igor/config.json

import json
from datetime import datetime
from pathlib import Path

from config import DEFAULT_THEME, DEFAULT_MODE, HISTORY_LIMIT

# ---------------- Пути ----------------
CONFIG_DIR = Path.home() / ".config" / "igor"
CONFIG_FILE = CONFIG_DIR / "config.json"

# ---------------- Значения по умолчанию ----------------
DEFAULTS = {
    "theme": DEFAULT_THEME,
    "mode": DEFAULT_MODE,
    "history": [],
    "history_limit": HISTORY_LIMIT,
}


class Settings:
    """Обёртка над JSON-файлом конфигурации."""

    def __init__(self):
        self.data = self._load()

    # ---------------- Загрузка / сохранение ----------------
    def _load(self):
        if not CONFIG_FILE.exists():
            return dict(DEFAULTS)
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                loaded = json.load(f)
            return {**DEFAULTS, **loaded}
        except Exception:
            return dict(DEFAULTS)

    def save(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ---------------- Доступ ----------------
    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    # ---------------- История ----------------
    def add_history(self, expression, result):
        entry = {
            "expr": expression,
            "result": result,
            "time": datetime.now().strftime("%H:%M:%S"),
        }
        history = self.data.setdefault("history", [])
        history.append(entry)
        limit = self.data.get("history_limit", HISTORY_LIMIT)
        if len(history) > limit:
            self.data["history"] = history[-limit:]
        self.save()

    def get_history(self):
        return self.data.get("history", [])

    def clear_history(self):
        self.data["history"] = []
        self.save()

    # ---------------- Удаление файла ----------------
    @staticmethod
    def delete_config():
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
            return True
        return False

    @staticmethod
    def config_path():
        return CONFIG_FILE
