def extended_gcd(a, b):  # Helps us reduce fractions
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1

    return gcd, x, y


class Fraction:
    def __init__(self, numerator, denominator):
        if denominator != 0:
            gcd, x, y = extended_gcd(numerator, denominator)
            self.numerator = int(numerator / gcd)
            self.denominator = int(denominator / gcd)
            self.actual_value = self.numerator / self.denominator
            self.print = "(" + str(self.numerator) + "/" + str(self.denominator) + ")"
            self.error = False
        else:
            self.error = True

    def __add__(self, other):
        if type(other) == int:
            fraction2 = Fraction(other, 1)
        elif isinstance(other, Fraction):
            fraction2 = other
        newNumerator = self.numerator * fraction2.denominator + fraction2.numerator * self.denominator
        return Fraction(newNumerator, self.denominator * fraction2.denominator)

    def __sub__(self, other):
        if type(other) == int:
            fraction2 = Fraction(other, 1)
        elif isinstance(other, Fraction):
            fraction2 = other
        newNumerator = self.numerator * fraction2.denominator - fraction2.numerator * self.denominator
        return Fraction(newNumerator, self.denominator * fraction2.denominator)

    def __mul__(self, other):
        if type(other) == float:
            fraction2 = Fraction(other, 1)
        if type(other) == int:
            fraction2 = Fraction(other, 1)
        elif isinstance(other, Fraction):
            fraction2 = other
        return Fraction(self.numerator * fraction2.numerator, self.denominator * fraction2.denominator)

    def __truediv__(self, other):
        if type(other) == int:
            fraction2 = Fraction(other, 1)
        elif isinstance(other, Fraction):
            fraction2 = other
        if fraction2.error:
            print("You are trying to divide by zero idiot")
        return Fraction(self.numerator * fraction2.denominator, self.denominator * fraction2.numerator)


class Node:  # I needed to access all of thee constants dynamically and this is the best I came up with
    def __init__(self, symbol):
        if symbol == "S":
            self.n1 = Fraction(2, 1)
            self.n2 = Fraction(1, 1)
            self.s1 = Fraction(3, 1)
            self.s2 = Fraction(2, 1)
        elif symbol == "L":
            self.n1 = Fraction(4, 1)
            self.n2 = Fraction(0, 1)
            self.s1 = Fraction(3, 1)
            self.s2 = Fraction(0, 1)
        elif symbol == "T":
            self.n1 = Fraction(4, 1)
            self.n2 = Fraction(2, 1)
            self.s1 = Fraction(1, 1)
            self.s2 = Fraction(0, 1)


def threading(constellation):
    [constant1, constant2] = [Fraction(1, 1), Fraction(0, 1)]
    for n in range(1, len(constellation)):
        prev_node = Node(constellation[n - 1])
        current_node = Node(constellation[n])
        factor1 = prev_node.s1 / current_node.n1
        constant1 = factor1 * constant1
        factor2 = (prev_node.s2 - current_node.n2) / current_node.n1
        constant2 = factor1 * constant2 + factor2
    return constant1, constant2


def get_each_node(Solutions_a_0, b, constellation):
    nodes = []
    a0 = b * Solutions_a_0[0] + Solutions_a_0[1]
    for element in range(0, len(constellation) - 1):
        next_node = Node(constellation[element + 1])
        current_node = Node(constellation[element])
        n = a0 * current_node.n1 + current_node.n2
        nodes.append(6 * n.actual_value + 4)
        a0 = (a0 * current_node.s1 + current_node.s2 - next_node.n2) / next_node.n1
    last_node = Node(constellation[len(constellation) - 1])
    n = last_node.n1 * a0 + last_node.n2
    nodes.append(6 * n.actual_value + 4)
    return nodes


# The extended Euclid algorithm gets us a solution, but it doesn't correspond to the solution with b=0. Granted, b=0 is
# not special objectively speaking, but it is convenient, so we find that solution using this
def find_first_solution(constant1, constant2):  # We find the first solution by brute force, I'm sorry
    for n in range(0, 2**63 - 1):
        k = constant1 * n + constant2
        if int(k.actualValue) == k.actualValue:
            return k.actualValue, n


constellation = "SSSLSSTTTT"
b = Fraction(0, 1)
constant1, constant2 = threading(constellation)
gcd, x0, y0 = extended_gcd(constant1.denominator, -constant1.numerator)
gcd_sign = gcd / abs(gcd)
# Solutions_a0 = [Fraction(-constant1.denominator/gcd,1),(constant2*y0*gcdSign)]
# Solutions_an = [Fraction(-constant1.numerator/gcd,1),(constant2*x0*gcdSign)]
[k, n] = find_first_solution(constant1, constant2)
solutions_a0 = [Fraction(constant1.denominator, 1), Fraction(n, 1)]
solutions_an = [Fraction(constant1.numerator, 1), Fraction(k, 1)]

print(
    "The equation for the constellation "
    + constellation
    + " is a_n = "
    + str(constant1.print)
    + " * a_0 + "
    + str(constant2.print)
)

print(
    "The solutions are: a_0 = "
    + str(solutions_a0[0].print)
    + " * b + "
    + str(solutions_a0[1].print)
    + ", a_n = "
    + str(solutions_an[0].print)
    + " * b + "
    + str(solutions_an[1].print)
)

print(
    "Finally, using b = "
    + str(b.print)
    + " we find that one example of this constellation is: "
    + str(get_each_node(solutions_a0, b, constellation))
)
