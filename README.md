# Python Calculator

This repository contains two versions of the calculator:

- `calculator.py` is a simple command-line calculator for learning Python input, output, and conditional logic.
- `calculator-gui.py` is a desktop graphical calculator with a user interface, keyboard support, expression history, and safer expression parsing.

## Calculator GUI

The GUI version is designed for a more practical desktop-app experience. It includes:

- Addition, subtraction, multiplication, and division
- Modulo (`%`) and power (`**`) operations
- Parentheses and decimal numbers
- Clear and backspace controls
- Keyboard input, including Enter to calculate, Escape to clear, and Backspace to delete
- A session history panel
- Error messages for invalid expressions and division by zero
- Restricted expression evaluation instead of unsafe `eval()` execution

The GUI accepts expressions such as:

```text
(12 + 8) * 3
2 ** 4
25 % 4
```

## How to Run

Python 3.8 or newer is recommended.

Run the command-line version:

```bash
python calculator.py
```

Run the graphical version:

```bash
python calculator-gui.py
```

Tkinter is included with most Python installations. On some Linux distributions, install it with:

```bash
sudo apt install python3-tk
```

## Difference Between the Two Versions

| Area | `calculator.py` | `calculator-gui.py` |
| --- | --- | --- |
| Interface | Terminal prompts | Desktop window with buttons and display |
| Input | One operation at a time | Full arithmetic expressions |
| Operations | `+`, `-`, `*`, `/` | `+`, `-`, `*`, `/`, `%`, `**`, parentheses, and unary signs |
| History | No saved history | Keeps calculations during the current session |
| Error handling | Prints an error message | Shows an error dialog |
| Best use | Python fundamentals and quick calculations | A more usable desktop application prototype |

The GUI is not a replacement for the original file. It builds on the same calculator idea while demonstrating a user interface, event handling, reusable functions, and application state.

## Libraries Used in the GUI

The current GUI uses only Python's standard library, so no `pip install` step is needed:

- `tkinter`: creates the window, display, buttons, history list, and dialogs.
- `ast`: parses an expression into a syntax tree without executing arbitrary Python code.
- `operator`: maps approved arithmetic operations to Python functions.

This separation is useful when designing Python apps: use a UI library for presentation, small focused modules for application logic, and a safe parser or domain library for the underlying behavior. Avoid choosing a large framework until the app needs the features it provides.

## Libraries to Consider for Future Development

Choose libraries based on the next product requirement:

- **`ttkbootstrap`**: modern themes and styling while keeping Tkinter's simple programming model.
- **`CustomTkinter`**: a more modern-looking desktop interface with themed widgets.
- **`PySide6`**: a full-featured Qt toolkit for polished cross-platform desktop applications, menus, layouts, and dialogs.
- **`PyQt6`**: another Qt option with a large widget ecosystem and strong designer tooling.
- **`Kivy`**: useful if the project should target touch devices or mobile platforms.
- **`SymPy`**: symbolic mathematics, equation solving, and more advanced calculator functions.
- **`NumPy`**: fast numerical operations when calculations become array-based or scientific.
- **`pytest`**: automated tests for arithmetic, parsing, invalid input, and future changes.
- **`black`** and **`ruff`**: consistent formatting and fast linting for maintainable Python code.

For the next iteration, `pytest` is a good first addition because it improves confidence without changing the user interface. If the main goal is a more polished desktop design, evaluate `CustomTkinter` or `PySide6` after separating the calculator logic from the GUI.

## Python Concepts Demonstrated

- Variables and functions
- Input and output
- Arithmetic operators
- `if`/`elif`/`else` statements
- Exception handling
- Classes and object-oriented structure
- Event-driven GUI programming
- Safe parsing of user input
