# Логика вычислений калькулятора — без привязки к интерфейсу

from config import ERROR_TEXT


class CalculatorEngine:
    """Хранит состояние (левое число, оператор, правое число)
    и выполняет арифметические операции."""

    def __init__(self):
        self.reset()

    # ---------------- Состояние ----------------
    def reset(self):
        """Полностью сбросить состояние (включая флаг ошибки)."""
        self.left_number = ""
        self.operation = ""
        self.right_number = ""
        self.is_error = False

    def get_display_text(self):
        """Строка, которую нужно показать на дисплее."""
        if self.is_error:
            return ERROR_TEXT
        return self.left_number + self.operation + self.right_number

    # ---------------- Ввод ----------------
    def add_digit(self, value):
        """Добавить цифру или точку в текущее число."""
        self._clear_error()
        if self.operation == "":
            self.left_number = self._append_digit(self.left_number, value)
        else:
            self.right_number = self._append_digit(self.right_number, value)

    def set_operator(self, value):
        """Запомнить оператор (если уже введено левое число)."""
        self._clear_error()
        if self.left_number != "":
            self.operation = value

    def backspace(self):
        """Удалить последний введённый символ."""
        self._clear_error()
        if self.right_number:
            self.right_number = self.right_number[:-1]
        elif self.operation:
            self.operation = ""
        elif self.left_number:
            self.left_number = self.left_number[:-1]

    def toggle_sign(self):
        """Переключить знак текущего числа (+/-)."""
        self._clear_error()
        if self.operation == "":
            self.left_number = self._flip_sign(self.left_number)
        else:
            self.right_number = self._flip_sign(self.right_number)

    def apply_percent(self):
        """Разделить текущее число на 100."""
        self._clear_error()
        try:
            if self.operation == "":
                self.left_number = self._format_result(float(self.left_number) / 100)
            else:
                self.right_number = self._format_result(float(self.right_number) / 100)
        except ValueError:
            # пустая строка или некорректное число — игнорируем
            pass

    # ---------------- Вычисление ----------------
    def calculate(self):
        """Вычислить результат и сохранить его как левое число."""
        # Если уже ошибка — не трогаем ничего
        if self.is_error:
            return
        if not (self.left_number and self.operation and self.right_number):
            return

        # Проверяем, что оба числа валидны (напр. "-" сам по себе — не число)
        try:
            float(self.left_number)
            float(self.right_number)
        except ValueError:
            return

        result = self._compute()
        if result is None:
            # Ошибка вычисления (например, деление на ноль)
            self.reset()
            self.is_error = True
            return

        self.left_number = self._format_result(result)
        self.operation = ""
        self.right_number = ""

    def _compute(self):
        """Чистая арифметика. Возвращает число или None при ошибке."""
        left = float(self.left_number)
        right = float(self.right_number)

        if self.operation == "+":
            return left + right
        if self.operation == "−":
            return left - right
        if self.operation == "×":
            return left * right
        if self.operation == "÷":
            if right == 0:
                return None          # ← деление на ноль
            return left / right
        return None

    # ---------------- Вспомогательные ----------------
    @staticmethod
    def _append_digit(current, value):
        """Добавить цифру/точку с защитой от повторов и ведущих нулей."""
        if value == ".":
            # Вторая точка в одном числе — игнорируем
            if "." in current:
                return current
            # Пусто или только минус — нужен ведущий ноль
            if current in ("", "-"):
                return current + "0."
            return current + "."
        # Заменяем одиночный ведущий ноль при вводе цифры ("0" + "5" → "5")
        if current in ("0", "-0"):
            return current[:-1] + value
        return current + value

    @staticmethod
    def _flip_sign(number):
        """Убрать или добавить минус в начале строки."""
        if number.startswith("-"):
            return number[1:]
        return "-" + number

    @staticmethod
    def _format_result(value):
        """Красиво отформатировать число: без .0 у целых, без шума float."""
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            return str(round(value, 10))
        return str(value)

    def _clear_error(self):
        """Любой ввод сбрасывает состояние ошибки."""
        if self.is_error:
            self.reset()
