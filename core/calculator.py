# Логика вычислений — без привязки к интерфейсу

import math

from config import ERROR_TEXT


class CalculatorEngine:
    """Хранит состояние (левое число, оператор, правое число)
    и выполняет арифметические операции."""

    def __init__(self):
        self.reset()

    # ---------------- Состояние ----------------
    def reset(self):
        self.left_number = ""
        self.operation = ""
        self.right_number = ""
        self.is_error = False

    def get_display_text(self):
        if self.is_error:
            return ERROR_TEXT
        return self.left_number + self.operation + self.right_number

    # ---------------- Ввод ----------------
    def add_digit(self, value):
        self._clear_error()
        if self.operation == "":
            self.left_number = self._append_digit(self.left_number, value)
        else:
            self.right_number = self._append_digit(self.right_number, value)

    def set_operator(self, value):
        self._clear_error()
        if self.left_number != "":
            self.operation = value

    def backspace(self):
        self._clear_error()
        if self.right_number:
            self.right_number = self.right_number[:-1]
        elif self.operation:
            self.operation = ""
        elif self.left_number:
            self.left_number = self.left_number[:-1]

    def toggle_sign(self):
        self._clear_error()
        if self.operation == "":
            self.left_number = self._flip_sign(self.left_number)
        else:
            self.right_number = self._flip_sign(self.right_number)

    def apply_percent(self):
        self._clear_error()
        try:
            if self.operation == "":
                self.left_number = self._format_result(
                    float(self.left_number) / 100
                )
            else:
                self.right_number = self._format_result(
                    float(self.right_number) / 100
                )
        except ValueError:
            pass

    def insert_constant(self, name):
        """Вставить π или e в текущее число."""
        self._clear_error()
        value = math.pi if name == "π" else math.e
        formatted = self._format_result(value)
        if self.operation == "":
            self.left_number = formatted
        else:
            self.right_number = formatted

    def load_value(self, value):
        """Загрузить число извне (для клика по истории)."""
        self.reset()
        self.left_number = str(value)

    # ---------------- Унарные операции ----------------
    def apply_unary(self, op):
        """Применить √, x², 1/x, log, ln, NOT к текущему числу."""
        self._clear_error()
        target = self.left_number if self.operation == "" else self.right_number

        if not target or target in ("-", ".", "-."):
            return

        try:
            value = float(target)
            result = self._unary_compute(op, value)
            if result is None:
                self.reset()
                self.is_error = True
                return
            formatted = self._format_result(result)
            if self.operation == "":
                self.left_number = formatted
            else:
                self.right_number = formatted
        except (ValueError, ZeroDivisionError):
            self.reset()
            self.is_error = True

    def _unary_compute(self, op, value):
        try:
            if op == "√":
                return math.sqrt(value) if value >= 0 else None
            if op == "x²":
                return value ** 2
            if op == "1/x":
                return None if value == 0 else 1 / value
            if op == "log":
                return math.log10(value) if value > 0 else None
            if op == "ln":
                return math.log(value) if value > 0 else None
            if op == "NOT":
                return ~int(value)
        except Exception:
            return None
        return None

    # ---------------- Вычисление ----------------
    def calculate(self):
        """Вернуть (выражение, результат) для истории, или None."""
        if self.is_error:
            return None
        if not (self.left_number and self.operation and self.right_number):
            return None

        try:
            float(self.left_number)
            float(self.right_number)
        except ValueError:
            return None

        expression = f"{self.left_number} {self.operation} {self.right_number}"
        result = self._compute()

        if result is None:
            self.reset()
            self.is_error = True
            return None

        formatted = self._format_result(result)
        self.left_number = formatted
        self.operation = ""
        self.right_number = ""
        return expression, formatted

    def _compute(self):
        left = float(self.left_number)
        right = float(self.right_number)
        op = self.operation

        # Базовая арифметика
        if op == "+":
            return left + right
        if op == "−":
            return left - right
        if op == "×":
            return left * right
        if op == "÷":
            return None if right == 0 else left / right

        # Расширенная арифметика
        if op == "xʸ":
            return left ** right
        if op == "MOD":
            return None if right == 0 else int(left) % int(right)

        # Финансовые операции
        if op == "+%":
            return left + left * right / 100
        if op == "-%":
            return left - left * right / 100

        # Побитовые операции
        if op == "AND":
            return int(left) & int(right)
        if op == "OR":
            return int(left) | int(right)
        if op == "XOR":
            return int(left) ^ int(right)
        if op == "«":
            return int(left) << int(right)
        if op == "»":
            return int(left) >> int(right)

        return None

    # ---------------- Вспомогательные ----------------
    @staticmethod
    def _append_digit(current, value):
        if value == ".":
            if "." in current:
                return current
            if current in ("", "-"):
                return current + "0."
            return current + "."
        if current in ("0", "-0"):
            return current[:-1] + value
        return current + value

    @staticmethod
    def _flip_sign(number):
        if number.startswith("-"):
            return number[1:]
        return "-" + number

    @staticmethod
    def _format_result(value):
        if isinstance(value, int):
            return str(value)
        if isinstance(value, float):
            if value != value:                             # NaN
                return "NaN"
            if value == float("inf"):
                return "∞"
            if value == float("-inf"):
                return "-∞"
            if value.is_integer() and abs(value) < 1e15:
                return str(int(value))
            if abs(value) >= 1e15 or (0 < abs(value) < 1e-6):
                return f"{value:.10g}"
            return str(round(value, 10))
        return str(value)

    def _clear_error(self):
        if self.is_error:
            self.reset()
