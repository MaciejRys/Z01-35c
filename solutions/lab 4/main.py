import sys;
class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None

    def execute_expression(self, expression):
        is_plus_or_minus = False
        is_multiplication_or_division = False
        for char in expression:
            if char == "+" or char == "-":
                self.data = char
                left_and_right_expression = expression.split(char, 1)
                self.left = Node()
                self.left.execute_expression(left_and_right_expression[0])
                self.right = Node()
                self.right.execute_expression(left_and_right_expression[1])
                is_plus_or_minus = True

        if not is_plus_or_minus:
            for char in expression:
                if char == "*" or char == "/":
                    self.data = char
                    left_and_right_expression = expression.split(char, 1)
                    self.left = Node()
                    self.left.execute_expression(left_and_right_expression[0])
                    self.right = Node()
                    self.right.execute_expression(left_and_right_expression[1])
                    is_multiplication_or_division = True

        if not is_plus_or_minus and not is_multiplication_or_division:
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

    def printNodes(self):
        if self.left is not None:
            print('(', end='')
            self.left.printNodes()
        print(self.data, end='')
        if self.right is not None:
            self.right.printNodes()
            print(')', end='')

if __name__ == '__main__':
    tree = Node()
    tree.execute_expression(sys.argv[1])
    print(tree.calculate())
    tree.printNodes()

