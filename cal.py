import tkinter as tk
from tkinter import scrolledtext
import re

def tokenize(expression):
    return re.findall(r'\d+|[+*/()-]', expression)

class Calculator:
    def __init__(self, expression):
        self.tokens = tokenize(expression)
        self.pos = 0

    def parse(self):
        return self.expr()

    def expr(self):
        result = self.term()
        while self.current_token() in ('+', '-'):
            op = self.current_token()
            self.next_token()
            if op == '+':
                result += self.term()
            elif op == '-':
                result -= self.term()
        return result

    def term(self):
        result = self.factor()
        while self.current_token() in ('*', '/'):
            op = self.current_token()
            self.next_token()
            if op == '*':
                result *= self.factor()
            elif op == '/':
                result /= self.factor()
        return result

    def factor(self):
        if self.current_token() == '(':
            self.next_token()
            result = self.expr()
            if self.current_token() == ')':
                self.next_token()  # Skip ')'
            else:
                raise ValueError("Mismatched parentheses")
            return result
        elif self.current_token().isdigit():
            result = int(self.current_token())
            self.next_token()
            return result
        else:
            raise ValueError("Unexpected token")

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def next_token(self):
        self.pos += 1

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hacker Calculator")
        self.create_widgets()

    def create_widgets(self):
        self.output = scrolledtext.ScrolledText(self.root, height=5, width=40, font=("Courier", 12), bg="black", fg="green")
        self.output.grid(row=0, column=0, columnspan=4)

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '(', ')', '+'
        ]
        row = 1
        col = 0
        for button in buttons:
            self.create_button(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.create_button('C', row, col)
        self.create_button('=', row, col + 1)

    def create_button(self, text, row, col):
        button = tk.Button(self.root, text=text, width=5, height=2, font=("Courier", 12), command=lambda t=text: self.on_button_click(t))
        button.grid(row=row, column=col, padx=5, pady=5)

    def on_button_click(self, text):
        if text == 'C':
            self.output.delete('1.0', tk.END)
        elif text == '=':
            try:
                expression = self.output.get('1.0', tk.END).strip()
                calculator = Calculator(expression)
                result = calculator.parse()
                self.output.delete('1.0', tk.END)
                self.output.insert(tk.END, str(result))
            except Exception as e:
                self.output.delete('1.0', tk.END)
                self.output.insert(tk.END, f"Error: {e}")
        else:
            self.output.insert(tk.END, text)

def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
