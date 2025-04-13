import sys
import re

def parse_equation(equation):
    terms = re.findall(r'([+-]?\s*\d*\.?\d+)\s*\*\s*X\^(\d+)', equation)
    coefficients = {}
    
    for term in terms:
        coef, power = term
        coef = float(coef.replace(' ', ''))
        power = int(power)
        coefficients[power] = coefficients.get(power, 0) + coef
    
    return coefficients

def reduced_form(coefficients):
    terms = [f'{coeff:+g} * X^{power}' for power, coeff in sorted(coefficients.items(), reverse=True) if coeff != 0]
    return ' '.join(terms).replace('+', ' +').replace('-', ' -')[1:] + ' = 0'

def solve_equation(coefficients):
    degree = max(coefficients.keys(), default=0)
    print(f'Polynomial degree: {degree}')
    
    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        return
    
    a = coefficients.get(2, 0)
    b = coefficients.get(1, 0)
    c = coefficients.get(0, 0)
    
    if degree == 0:
        print("No variable found. The equation is trivial.")
        return
    
    if degree == 1:
        if b == 0:
            print("No solution.")
        else:
            solution = -c / b
            print(f'The solution is: {solution:.6g}')
    
    if degree == 2:
        discriminant = b**2 - 4*a*c
        if discriminant > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            sol1 = (-b + discriminant**0.5) / (2*a)
            sol2 = (-b - discriminant**0.5) / (2*a)
            print(f'{sol1:.6g}, {sol2:.6g}')
        elif discriminant == 0:
            print("Discriminant is zero, the solution is:")
            sol = -b / (2*a)
            print(f'{sol:.6g}')
        else:
            print("Discriminant is strictly negative, no real solutions.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./computor \"equation\"")
        sys.exit(1)
    
    equation = sys.argv[1].replace(' ', '')
    left, right = equation.split('=')
    
    left_coeffs = parse_equation(left)
    right_coeffs = parse_equation(right)
    
    for key in right_coeffs:
        left_coeffs[key] = left_coeffs.get(key, 0) - right_coeffs[key]
    
    print(f'Reduced form: {reduced_form(left_coeffs)}')
    solve_equation(left_coeffs)
