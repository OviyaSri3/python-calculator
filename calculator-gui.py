"""A beginner-friendly graphical calculator built with Python's standard library."""  # Explain what this file contains.

import ast  # Read mathematical expressions as a safe syntax tree.
import operator  # Use Python's arithmetic functions without using unsafe eval().
import tkinter as tk  # Build the window and all of its widgets.
from tkinter import messagebox  # Show a small dialog when the user makes an error.


# Store the arithmetic operations that the calculator is allowed to perform.
ALLOWED_OPERATORS = {
    ast.Add: operator.add,  # Handle addition, such as 2 + 3.
    ast.Sub: operator.sub,  # Handle subtraction, such as 5 - 2.
    ast.Mult: operator.mul,  # Handle multiplication, such as 4 * 3.
    ast.Div: operator.truediv,  # Handle division, such as 8 / 2.
    ast.Mod: operator.mod,  # Handle remainders, such as 7 % 3.
    ast.Pow: operator.pow,  # Handle powers, such as 2 ** 3.
    ast.USub: operator.neg,  # Handle negative numbers, such as -5.
    ast.UAdd: operator.pos,  # Handle positive numbers, such as +5.
}  # End the allowed-operation table.


def calculate_expression(expression):  # Convert a typed expression into a numeric answer.
    """Evaluate only simple arithmetic, rather than executing arbitrary Python code."""  # Explain the safety goal.
    tree = ast.parse(expression, mode="eval")  # Parse the text as one expression.

    def evaluate(node):  # Recursively calculate one part of the syntax tree.
        if isinstance(node, ast.Expression):  # Check whether this is the tree wrapper.
            return evaluate(node.body)  # Continue with the actual expression inside it.
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):  # Allow numbers only.
            return node.value  # Return the number found in the expression.
        if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:  # Allow known binary operators.
            left = evaluate(node.left)  # Calculate the value on the left side.
            right = evaluate(node.right)  # Calculate the value on the right side.
            if isinstance(node.op, ast.Pow) and abs(right) > 100:  # Prevent accidentally huge powers.
                raise ValueError("The power must be between -100 and 100.")  # Explain the input limit.
            return ALLOWED_OPERATORS[type(node.op)](left, right)  # Apply the selected operation.
        if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPERATORS:  # Allow +number and -number.
            return ALLOWED_OPERATORS[type(node.op)](evaluate(node.operand))  # Apply the sign to the number.
        raise ValueError("Use numbers, parentheses, and + - * / % ** only.")  # Reject everything else.

    return evaluate(tree)  # Return the final calculated value.


class CalculatorApp:  # Group the window and its behavior in one reusable class.
    def __init__(self, window):  # Set up the calculator when the app starts.
        self.window = window  # Keep a reference to the main window.
        self.window.title("Python Calculator")  # Set the text shown in the title bar.
        self.window.geometry("760x520")  # Give the first window a comfortable size.
        self.window.minsize(560, 420)  # Stop the window becoming too small to use.
        self.window.configure(bg="#18212b")  # Set a dark blue-gray background.
        self.expression = tk.StringVar()  # Hold the text currently shown in the display.
        self.history = []  # Keep completed calculations for this session.
        self.build_interface()  # Create all visible widgets.
        self.bind_keyboard()  # Add keyboard shortcuts after the widgets exist.

    def build_interface(self):  # Create and arrange the calculator controls.
        main_frame = tk.Frame(self.window, bg="#18212b", padx=18, pady=18)  # Create the main page area.
        main_frame.pack(fill="both", expand=True)  # Make the page fill the window.
        main_frame.columnconfigure(0, weight=3)  # Give the calculator most of the horizontal space.
        main_frame.columnconfigure(1, weight=2)  # Give the history panel the remaining space.
        main_frame.rowconfigure(1, weight=1)  # Let the content row expand vertically.

        title = tk.Label(main_frame, text="PYTHON CALCULATOR", font=("DejaVu Sans", 20, "bold"), fg="#f4f7fa", bg="#18212b")  # Create the heading.
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))  # Place the heading above both panels.

        calculator_frame = tk.Frame(main_frame, bg="#22303d", padx=14, pady=14)  # Create the calculator panel.
        calculator_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))  # Place it on the left.
        calculator_frame.columnconfigure(0, weight=1)  # Let the button columns resize evenly.
        calculator_frame.columnconfigure(1, weight=1)  # Let the button columns resize evenly.
        calculator_frame.columnconfigure(2, weight=1)  # Let the button columns resize evenly.
        calculator_frame.columnconfigure(3, weight=1)  # Let the button columns resize evenly.

        display = tk.Entry(calculator_frame, textvariable=self.expression, font=("DejaVu Sans", 24), justify="right", state="readonly", readonlybackground="#f4f7fa", fg="#18212b", relief="flat", bd=0)  # Create the calculator display.
        display.grid(row=0, column=0, columnspan=4, sticky="ew", ipady=14, pady=(0, 14))  # Place the display across all columns.

        button_layout = [  # Define the button labels and their positions.
            [("C", "clear", "#e06c75"), ("⌫", "backspace", "#d19a66"), ("(", "(", "#61afef"), (")", ")", "#61afef")],  # Add editing and parentheses buttons.
            [("7", "7", "#304354"), ("8", "8", "#304354"), ("9", "9", "#304354"), ("/", "/", "#61afef")],  # Add the first number row.
            [("4", "4", "#304354"), ("5", "5", "#304354"), ("6", "6", "#304354"), ("*", "*", "#61afef")],  # Add the second number row.
            [("1", "1", "#304354"), ("2", "2", "#304354"), ("3", "3", "#304354"), ("-", "-", "#61afef")],  # Add the third number row.
            [("0", "0", "#304354"), (".", ".", "#304354"), ("%", "%", "#61afef"), ("+", "+", "#61afef")],  # Add the final number row.
            [("**", "**", "#61afef"), ("=", "equals", "#98c379")],  # Add power and answer buttons.
        ]  # Finish the button layout.

        for row_number, row in enumerate(button_layout, start=1):  # Visit each row of button definitions.
            for column_number, (label, action, color) in enumerate(row):  # Visit each button in this row.
                button = tk.Button(calculator_frame, text=label, command=lambda value=action: self.handle_button(value), font=("DejaVu Sans", 14, "bold"), bg=color, fg="#18212b", activebackground="#ffffff", relief="flat", bd=0, cursor="hand2")  # Create one clickable button.
                button.grid(row=row_number, column=column_number, columnspan=2 if label in ("**", "=") else 1, sticky="nsew", padx=3, pady=3, ipady=9)  # Put the button into the grid.
            calculator_frame.rowconfigure(row_number, weight=1)  # Let each button row grow evenly.

        history_frame = tk.Frame(main_frame, bg="#22303d", padx=14, pady=14)  # Create the history panel.
        history_frame.grid(row=1, column=1, sticky="nsew")  # Place it on the right.
        history_frame.rowconfigure(1, weight=1)  # Let the list expand vertically.
        history_frame.columnconfigure(0, weight=1)  # Let the list expand horizontally.
        history_title = tk.Label(history_frame, text="HISTORY", font=("DejaVu Sans", 12, "bold"), fg="#f4f7fa", bg="#22303d")  # Create the history heading.
        history_title.grid(row=0, column=0, sticky="w", pady=(0, 8))  # Place the heading above the list.
        self.history_list = tk.Listbox(history_frame, font=("DejaVu Sans", 11), bg="#18212b", fg="#d8dee9", selectbackground="#61afef", selectforeground="#18212b", relief="flat", bd=0, activestyle="none")  # Create the history list.
        self.history_list.grid(row=1, column=0, sticky="nsew")  # Place the list below its heading.
        clear_history = tk.Button(history_frame, text="Clear history", command=self.clear_history, font=("DejaVu Sans", 10), bg="#304354", fg="#f4f7fa", activebackground="#61afef", relief="flat", bd=0, cursor="hand2")  # Create a history reset button.
        clear_history.grid(row=2, column=0, sticky="ew", pady=(10, 0), ipady=7)  # Place the reset button under the list.

    def bind_keyboard(self):  # Connect useful keyboard keys to calculator actions.
        self.window.bind("<Return>", lambda event: self.handle_button("equals"))  # Make Enter calculate.
        self.window.bind("<Escape>", lambda event: self.handle_button("clear"))  # Make Escape clear the display.
        self.window.bind("<BackSpace>", lambda event: self.handle_button("backspace"))  # Make Backspace delete one character.
        self.window.bind("<Key>", self.handle_key)  # Send typed characters to the calculator.

    def handle_key(self, event):  # Decide whether a typed key belongs in the expression.
        if event.char in "0123456789.+-*/%()":  # Accept normal arithmetic characters.
            self.expression.set(self.expression.get() + event.char)  # Add the character to the display.
        elif event.char == "^":  # Support the familiar caret as a power shortcut.
            self.expression.set(self.expression.get() + "**")  # Convert caret into Python's power operator.
        return "break"  # Prevent the read-only Entry from handling the key itself.

    def handle_button(self, action):  # Perform the action requested by a button.
        if action == "clear":  # Check whether the clear button was pressed.
            self.expression.set("")  # Remove everything from the display.
        elif action == "backspace":  # Check whether the backspace button was pressed.
            self.expression.set(self.expression.get()[:-1])  # Remove the last character.
        elif action == "equals":  # Check whether the equals button was pressed.
            self.calculate()  # Calculate and display the answer.
        else:  # Handle a number, operator, decimal, or parenthesis.
            self.expression.set(self.expression.get() + action)  # Add the button text to the display.

    def calculate(self):  # Calculate the current expression and update the interface.
        expression = self.expression.get().strip()  # Read and trim the display text.
        if not expression:  # Check whether the display is empty.
            return  # Do nothing when there is nothing to calculate.
        try:  # Start a block that can catch invalid user input.
            result = calculate_expression(expression)  # Use the safe expression calculator above.
            result_text = str(round(result, 12))  # Keep floating-point answers readable.
            self.history.append(f"{expression} = {result_text}")  # Save this calculation in memory.
            self.history_list.insert(tk.END, self.history[-1])  # Show the newest calculation in the list.
            self.expression.set(result_text)  # Put the answer back into the display.
        except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError) as error:  # Catch expected calculator errors.
            messagebox.showerror("Invalid calculation", str(error) or "Please check your expression.")  # Explain the problem in a dialog.

    def clear_history(self):  # Remove all saved calculations from this session.
        self.history.clear()  # Empty the Python list.
        self.history_list.delete(0, tk.END)  # Empty the visible list.


def main():  # Start the graphical application.
    window = tk.Tk()  # Create the main application window.
    CalculatorApp(window)  # Build the calculator inside that window.
    window.mainloop()  # Keep the window open until the user closes it.


if __name__ == "__main__":  # Run the GUI only when this file is started directly.
    main()  # Launch the calculator application.