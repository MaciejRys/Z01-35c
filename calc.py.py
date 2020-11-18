import sys, math
import tkinter as tk

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None

    def execute_expression(self, expression):
        is_in_bracket = False

        for char in expression:
            if char == "(":
                is_in_bracket = True
            if char == ")":
                is_in_bracket = False

            if (char == "+" or char == "-") and is_in_bracket == False:
                self.data = char
                left_and_right_expression = expression.split(char, 1)
                self.left = Node()
                self.left.execute_expression(left_and_right_expression[0])
                self.right = Node()
                self.right.execute_expression(left_and_right_expression[1])
                return True

        for char in expression:
            if char == "(":
                is_in_bracket = True
            if char == ")":
                is_in_bracket = False
            if (char == "*" or char == "/") and is_in_bracket == False:
                self.data = char
                left_and_right_expression = expression.split(char, 1)
                self.left = Node()
                self.left.execute_expression(left_and_right_expression[0])
                self.right = Node()
                self.right.execute_expression(left_and_right_expression[1])
                return True
        i = 0
        for char in expression:
            if char == "(":
                is_in_bracket = True
            if char == ")":
                is_in_bracket = False

            if (char == "^") and is_in_bracket == False:
                self.data = char
                left_and_right_expression = expression.split(char, 1)
                self.left = Node()
                self.left.execute_expression(left_and_right_expression[0])
                self.right = Node()
                self.right.execute_expression(left_and_right_expression[1])
                return True
            elif char == "s" and is_in_bracket == False:
                self.data = expression
                return True
            elif (char == "%") and is_in_bracket == False:
                self.data = char
                left_and_right_expression = expression.split(char, 1)
                self.left = Node()
                self.left.execute_expression(left_and_right_expression[0])
                self.right = Node()
                self.right.execute_expression(left_and_right_expression[1])
                return True
            elif char == "l" and is_in_bracket == False:
                self.data = expression
                return True
            elif char == "a" and is_in_bracket == False:
                self.data = expression
                return True
            elif char == "!" and is_in_bracket == False:
                self.data = expression
                return True
            i += 1


        if expression[0] == "(":
            expression = expression[1:-1]
            self.execute_expression(expression)
            return True

        try:
            self.data = float(expression)
        except ValueError:
            return False
        return True

    def calculate(self):
        try:
            float(self.data)
            return float(self.data)
        except ValueError:
            if self.data == "*":
                return self.left.calculate() * self.right.calculate()
            if self.data == "/":
                return self.left.calculate() / self.right.calculate()
            if self.data == "+":
                return self.left.calculate() + self.right.calculate()
            if self.data == "-":
                return self.left.calculate() - self.right.calculate()
            if self.data == "^":
                return self.left.calculate() ** self.right.calculate()
            if self.data == "%":
                return self.left.calculate() % self.right.calculate()
            if self.data[0] == "a":
                return abs(float(self.data[4:-1]))
            if self.data[0] == "l":
                return math.log10(float(self.data[4:-1]))
            if self.data[0] == "s":
                return math.sqrt(float(self.data[5:-1]))
            if self.data[-1] == "!":
                return math.factorial(float(self.data[0:-1]))

    def printNodes(self, napis, start):

        start += " "
        if self.left is not None:
            self.left.printNodes(start + napis + "─", start)
        print(start + napis + "  " + str(self.data))
        if self.right is not None:
            self.right.printNodes(start + napis + "─", start)

root = tk.Tk()
expression = ""
tree = Node()

def DrawMainLayout():

    global mainLabel
    mainLabel= tk.Label(root,text="",font=("Helvetica", 36),relief="raised",anchor="e")
    mainLabel.grid(row=0,columnspan=4,sticky="EW")

    button = tk.Button(root, text="^",font=("Helvetica", 16),command=lambda:AddToExpression("^"))
    button.grid(row=1,column=0,sticky="nsew")

    button = tk.Button(root,text="x!",font=("Helvetica", 16),command=lambda:AddToExpression("!"))
    button.grid(row=1,column=1,sticky="nesw")

    button = tk.Button(root,text="sqrt(x)",font=("Helvetica", 16),command=lambda:AddToExpression("sqrt("))
    button.grid(row=1,column=2,sticky="nesw")

    button = tk.Button(root, text="1",font=("Helvetica", 16),command=lambda:AddToExpression("1"))
    button.grid(row=2,column=0,sticky="nsew")

    button = tk.Button(root, text="2",font=("Helvetica", 16),command=lambda:AddToExpression("2"))
    button.grid(row=2,column=1,sticky="nsew")

    button = tk.Button(root, text="3",font=("Helvetica", 16),command=lambda:AddToExpression("3"))
    button.grid(row=2,column=2,sticky="nsew")

    button = tk.Button(root, text="4",font=("Helvetica", 16),command=lambda:AddToExpression("4"))
    button.grid(row=3,column=0,sticky="nsew")

    button = tk.Button(root, text="5",font=("Helvetica", 16),command=lambda:AddToExpression("5"))
    button.grid(row=3,column=1,sticky="nsew")

    button = tk.Button(root, text="6",font=("Helvetica", 16),command=lambda:AddToExpression("6"))
    button.grid(row=3,column=2,sticky="nsew")

    button = tk.Button(root, text="7",font=("Helvetica", 16),command=lambda:AddToExpression("7"))
    button.grid(row=4,column=0,sticky="nsew")

    button = tk.Button(root, text="8",font=("Helvetica", 16),command=lambda:AddToExpression("8"))
    button.grid(row=4,column=1,sticky="nsew")

    button = tk.Button(root, text="9",font=("Helvetica", 16),command=lambda:AddToExpression("9"))
    button.grid(row=4,column=2,sticky="nsew")

    button = tk.Button(root, text="+",font=("Helvetica", 16),command=lambda:AddToExpression("+"))
    button.grid(row=1,column=3,sticky="nsew")

    button = tk.Button(root, text="-",font=("Helvetica", 16),command=lambda:AddToExpression("-"))
    button.grid(row=2,column=3,sticky="nsew")

    button = tk.Button(root, text="*",font=("Helvetica", 16),command=lambda:AddToExpression("*"))
    button.grid(row=3,column=3,sticky="nsew")

    button = tk.Button(root, text="/",font=("Helvetica", 16),command=lambda:AddToExpression("/"))
    button.grid(row=4,column=3,sticky="nsew")

    button = tk.Button(root, text="(",font=("Helvetica", 16),command=lambda:AddToExpression("("))
    button.grid(row=5,column=0,sticky="nsew")

    button = tk.Button(root, text=")",font=("Helvetica", 16),command=lambda:AddToExpression(")"))
    button.grid(row=5,column=1,sticky="nsew")

    button = tk.Button(root,text="%",font=("Helvetica", 16),command=lambda:AddToExpression("%"))
    button.grid(row=5,column=2,sticky="nesw")

    button = tk.Button(root,text="log(x)",font=("Helvetica", 16),command=lambda:AddToExpression("log("))
    button.grid(row=5,column=3,sticky="nesw")

    button = tk.Button(root,text="=",font=("Helvetica", 16),command=Solve)
    button.grid(row=6,column=0,columnspan=2,sticky="nesw")

    button = tk.Button(root,text="<--",font=("Helvetica", 16),command=RemoveOneChar)
    button.grid(row=6,column=2,sticky="nesw")

    button = tk.Button(root,text="C",font=("Helvetica", 16),command=RemoveAll)
    button.grid(row=6,column=3,sticky="nesw")

    button = tk.Button(root,text=".",font=("Helvetica", 16),command=lambda:AddToExpression("."))
    button.grid(row=7,column=0,columnspan=2,sticky="nesw")

    button = tk.Button(root,text="0",font=("Helvetica", 16),command=lambda:AddToExpression("0"))
    button.grid(row=7,column=2,sticky="nesw")

    button = tk.Button(root,text="abs(x)",font=("Helvetica", 16),command=lambda:AddToExpression("abs("))
    button.grid(row=7,column=3,sticky="nesw")
def AddToExpression(txt):
    global expression
    expression += txt
    mainLabel["text"] = expression

def Solve():
    global expression
    tree.execute_expression(expression)
    tree.printNodes("├──", "   ")
    expression = tree.calculate()
    mainLabel["text"] = expression

def RemoveAll():
    global expression
    expression = ""
    mainLabel["text"] = expression
def RemoveOneChar():
    global expression
    expression = expression[:-1]
    mainLabel["text"] = expression


if __name__ == '__main__':
    root.geometry("500x650")
    root.resizable(height=False, width=False)
    DrawMainLayout()
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_rowconfigure(6, weight=1)
    root.grid_rowconfigure(7, weight=1)
    root.mainloop()







