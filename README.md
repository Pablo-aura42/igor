# igor 🧮

> A tiny calculator with big ambitions — Python + CustomTkinter.

[🇷🇺 Русская версия](README.ru.md)

A minimalist desktop calculator with 12 color themes, 4 modes, calculation history and persistent settings. Built with Python and CustomTkinter.

![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2%2B-1f6aa5)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📸 Screenshot

<!-- Replace with a real screenshot when ready -->
<!-- ![igor screenshot](docs/screenshot.png) -->

*Coming soon.*

---

## ✨ Features

- 🎨 **12 color themes** — Catppuccin (Mocha, Macchiato, Frappé, Latte), Nord, Ayu (Dark, Mirage), Dracula, Tokyo Night, Gruvbox Dark, One Dark, Solarized Dark — switchable on the fly
- 🎛️ **4 modes** — simple, advanced, financial, programming
- 📜 **Calculation history** — click any entry to insert its result back into the display
- 💾 **Persistent config** in `~/.config/igor/config.json` — theme, mode and history survive restarts
- ⌨️ **Hotkeys** — digits, operators, `Enter`, `Backspace`, `Esc`, `Ctrl+L`, `Ctrl+H`, `Ctrl+Q`
- 🖱️ **Hover effects** — each button category has its own highlight color
- 🧠 **Error handling** — division by zero, square root of a negative, log of a non-positive and more show a red "Ошибка"
- 🎯 **Input protection** — no double dots, no leading zeros, `Backspace` removes one character at a time

---

## 🎛️ Modes

| Mode | Operations |
|---|---|
| **Simple** | `+ − × ÷ %`, `±`, `⌫`, `C` |
| **Advanced** | + `√`, `x²`, `xʸ`, `1/x`, `log`, `π`, `e` |
| **Financial** | + `+%`, `-%` (add/subtract a percentage of the left operand) |
| **Programming** | + `AND`, `OR`, `XOR`, `NOT`, `«`, `»`, `MOD` |

Switch via the **Режим** menu, or edit the layouts directly in `config.py` (all layouts are defined as constants).

---

## 🎨 Themes

All themes live directly in code (`core/themes.py`), no external JSON files. Adding a new one is just a `dict` entry in `THEMES`.

<details>
<summary>Available themes</summary>

- Catppuccin Mocha
- Catppuccin Macchiato
- Catppuccin Frappé
- Catppuccin Latte
- Catppuccin Mocha (Light)
- Nord
- Ayu Dark
- Ayu Mirage
- Dracula
- Tokyo Night
- Gruvbox Dark
- One Dark
- Solarized Dark

</details>

---

## ⌨️ Hotkeys

| Key | Action |
|---|---|
| `0`–`9` | digits |
| `.` / `,` | decimal point |
| `+` `-` `*` `/` | operators (`-` → `−`, `*` → `×`, `/` → `÷`) |
| `^` | power (`xʸ`, advanced mode) |
| `%` | percent |
| `Enter` / `KP_Enter` | equals |
| `BackSpace` | delete one character |
| `Esc` / `Delete` | clear |
| `Ctrl+L` | clear |
| `Ctrl+H` | open history |
| `Ctrl+Q` | quit |

---

## 🚀 Installation

### Requirements

- Python 3.10+
- Linux / macOS / Windows

### Steps

```bash
git clone https://github.com/Pablo-aura42/igor.git
cd igor

python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
python main.py
```

---

## 📁 Project structure

```
igor/
├── main.py                  # entry point
├── config.py                # constants, layouts, modes
├── requirements.txt
├── core/
│   ├── calculator.py        # calculation engine (Tkinter-free)
│   ├── settings.py          # config load/save
│   └── themes.py            # 12 color themes + ThemeManager
└── ui/
    ├── app.py               # main window: glues everything together
    ├── display.py           # display widget
    ├── button_panel.py      # button grid (rebuilt per mode)
    ├── menu_bar.py          # custom menu bar themed with the app
    ├── history_dialog.py    # history window
    └── about_dialog.py      # "About" window
```

**Principle:** `core/` knows nothing about Tkinter, `ui/` knows nothing about math. `app.py` glues them together. So logic can be tested separately, and UI can be redesigned without breaking calculations.

---

## 💾 Configuration

All settings are stored in:

```
~/.config/igor/config.json
```

Contents:

- current theme (`theme`)
- current mode (`mode`)
- calculation history (`history`, 50 entries by default)

Delete the config via **Справка → О программе → Удалить конфиг**, or manually:

```bash
rm ~/.config/igor/config.json
```

---

## 🛠️ Development

No external dependencies other than `customtkinter`. Everything else is the standard library.

Want to contribute? A few ideas:

- [ ] Screenshot in README
- [ ] Scientific mode with trigonometry
- [ ] Base switching (HEX/DEC/OCT/BIN) in Programming mode
- [ ] Live theme switching for already-open dialogs
- [ ] Tests for `core/calculator.py` (pytest)

PRs welcome — but this is a learning project first, so don't be upset if something sits around for a while.

---

## 📄 License

MIT — do whatever you want, just credit the author.

---

[🇷🇺 Читать по-русски](README.ru.md)
