# Настройки внешнего вида, режимов и раскладки калькулятора

# ---------------- Окно ----------------
APP_TITLE = "igor"
APP_WIDTH = 360
APP_HEIGHT = 640

# ---------------- Шрифты ----------------
DISPLAY_FONT = ("Segoe UI", 32)
BUTTON_FONT = ("Segoe UI", 20)

# ---------------- Размеры ----------------
DISPLAY_HEIGHT = 80
BUTTON_HEIGHT = 60
BUTTON_WIDTH = 70
CORNER_RADIUS = 12

# ---------------- Отступы ----------------
PADDING_OUTER = 20
PADDING_INNER = 6

# ---------------- Категории операций ----------------
BINARY_OPERATORS = [
    "+", "−", "×", "÷", "xʸ", "MOD",
    "AND", "OR", "XOR", "«", "»", "+%", "-%",
]
UNARY_OPERATORS = ["√", "x²", "1/x", "log", "ln", "NOT"]
CONSTANTS = ["π", "e"]

# Обратная совместимость с ButtonPanel: чтобы классификация кнопок работала
OPERATORS = BINARY_OPERATORS

# ---------------- Раскладки по режимам ----------------
_LAYOUT_SIMPLE = [
    ["⌫"],
    ["C", "±", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["0", ".", "="],
]

_LAYOUT_ADVANCED = [
    ["⌫"],
    ["C", "±", "√", "x²", "÷"],
    ["7", "8", "9", "xʸ", "×"],
    ["4", "5", "6", "1/x", "−"],
    ["1", "2", "3", "π", "+"],
    ["0", ".", "e", "log", "="],
]

_LAYOUT_FINANCIAL = [
    ["⌫"],
    ["C", "+%", "-%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["0", ".", "%", "="],
]

_LAYOUT_PROGRAMMING = [
    ["⌫"],
    ["C", "±", "AND", "OR", "÷"],
    ["7", "8", "9", "XOR", "×"],
    ["4", "5", "6", "MOD", "−"],
    ["1", "2", "3", "«", "+"],
    ["0", ".", "NOT", "»", "="],
]

MODES = {
    "simple": {
        "title": "Простой",
        "columns": 4,
        "layout": _LAYOUT_SIMPLE,
    },
    "advanced": {
        "title": "Расширенный",
        "columns": 5,
        "layout": _LAYOUT_ADVANCED,
    },
    "financial": {
        "title": "Финансовый",
        "columns": 4,
        "layout": _LAYOUT_FINANCIAL,
    },
    "programming": {
        "title": "Программирование",
        "columns": 5,
        "layout": _LAYOUT_PROGRAMMING,
    },
}

DEFAULT_MODE = "simple"

# ---------------- Тема по умолчанию ----------------
DEFAULT_THEME = "Catppuccin Mocha"

# ---------------- Текст ошибки ----------------
ERROR_TEXT = "Ошибка"

# ---------------- Лимит истории ----------------
HISTORY_LIMIT = 50
