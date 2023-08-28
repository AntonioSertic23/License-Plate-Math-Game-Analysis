import math
import cmath
import itertools
import csv

# 1. Getting all license plates
def generate_registrations():
    registrations = []
    for i in range(10000):
        # Adding leading zeros to the number if it's less than 1000
        number = str(i).zfill(4)
        registrations.append(number)
    return registrations

all_registrations = generate_registrations()

# 2. Defining all operations
def addition(a, b):
    return a + b

def subtraction(a, b):
    return a - b

def multiplication(a, b):
    return a * b

def division(numerator, denominator):
    if denominator != 0:
        result = numerator / denominator
        if not math.isinf(result) and not math.isnan(result):
            return result

    return None

# Desired maximum exponent value
MAX_EXPONENTIAL_VALUE = 10**2
def squaring(a, b):
    if b <= MAX_EXPONENTIAL_VALUE:
        try:
            result = a ** b
            if math.isfinite(result):
                return None
        except Exception:
            return None

    return None

def root(a, b):
    # (1) The square root can only be calculated for positive numbers as taking the square root of a negative number results in complex numbers
    # (2) If number 'a' is even, its square root will be an imaginary number
    if a > 0 and a % 2 == 1:
        temp = squaring(b, (1/a))
        if temp != None:
            result = temp
            if cmath.isclose(result.imag, 0.0):
                return result.real

    return None

binary_operations = [addition, subtraction, multiplication, division, squaring, root]

def raw_number(number):
    return number

def negate_number(number):
    return number * -1

# Desired maximum factorial value
MAX_FACTORIAL_VALUE = 10**2
def factorial(number):
    if number >= 0 and number <= MAX_FACTORIAL_VALUE:
        try:
            result = math.factorial(number)
            return result
        except Exception:
            return None
    
    return None

unary_operations = [raw_number, negate_number, factorial]

operator_precedence = {
    "squaring": 4,
    "root": 3,
    "multiplication": 2,
    "division": 2,
    "addition": 1,
    "subtraction": 1,
}

signs = {
    addition: '+',
    subtraction: '-',
    multiplication: '*',
    division: '/',
    squaring: 'pow',
    root: 'sqrt'
}

# 3. Function for creating formulas
def Equation(z1, o1, f1, z2, o2, f2, z3, o3, z4, parentheses):
    first_function_sign = signs.get(f1, '')
    second_function_sign = signs.get(f2, '')

    z1prefix = "-" if o1.__name__ == 'negate_number' and z1 != 0 else ""
    z1suffix = "!" if o1.__name__ == 'factorial' else ""

    z2prefix = "-" if o2.__name__ == 'negate_number' and z1 != 0 else ""
    z2suffix = "!" if o2.__name__ == 'factorial' else ""

    z3prefix = "-" if o3.__name__ == 'negate_number' and z1 != 0 else ""
    z3suffix = "!" if o3.__name__ == 'factorial' else ""

    if parentheses == 1:
        return f"({z1prefix}{z1}{z1suffix} {first_function_sign} {z2prefix}{z2}{z2suffix}) {second_function_sign} {z3prefix}{z3}{z3suffix} = {z4}"
    elif parentheses == 2:
        return f"{z1prefix}{z1}{z1suffix} {first_function_sign} ({z2prefix}{z2}{z2suffix} {second_function_sign} {z3prefix}{z3}{z3suffix}) = {z4}"
    else:
        return f"{z1prefix}{z1}{z1suffix} {first_function_sign} {z2prefix}{z2}{z2suffix} {second_function_sign} {z3prefix}{z3}{z3suffix} = {z4}"

# 4. Checking all license plates
solution_list = []
def perform_operations():

    # for each license plate...
    for plate_num in all_registrations:
        total_num = 0
        solution = None

        # for each combination of unary operations...
        product_unary_operations =  itertools.product(unary_operations, repeat=3)
        for prod_u in product_unary_operations:
            
            # for each combination of binary operations...
            product_binary_operations =  itertools.product(binary_operations, repeat=2)
            for prod_b in product_binary_operations:
                
                # CASE 1: when the parenthesis is in the first place
                result1 = prod_b[0](int(prod_u[0](int(plate_num[0]))), int(prod_u[1](int(plate_num[1]))))
                if result1 == None:
                    continue
                result2 = prod_b[1](result1, int(prod_u[2](int(plate_num[2]))))
                if result2 == None:
                    continue
                else:
                    if result2 == int(plate_num[3]):
                        total_num += 1
                        solution = Equation(
                            int(plate_num[0]),
                            prod_u[0],
                            prod_b[0],
                            int(plate_num[1]),
                            prod_u[1],
                            prod_b[1],
                            int(plate_num[2]),
                            prod_u[2],
                            int(plate_num[3]),
                            1
                        )

                # CASE 2: when the parenthesis is in the second place
                result1 = prod_b[1](int(prod_u[1](int(plate_num[1]))), int(prod_u[2](int(plate_num[2]))))
                if result1 == None:
                    continue
                result2 = prod_b[0](int(prod_u[0](int(plate_num[0]))), result1)
                if result2 == None:
                    continue
                else:
                    if result2 == int(plate_num[3]):
                        total_num += 1
                        solution = Equation(
                            int(plate_num[0]),
                            prod_u[0],
                            prod_b[0],
                            int(plate_num[1]),
                            prod_u[1],
                            prod_b[1],
                            int(plate_num[2]),
                            prod_u[2],
                            int(plate_num[3]),
                            2
                        )

                # CASE 3: when there are no parentheses, priority is considered
                if operator_precedence[prod_b[0].__name__] < operator_precedence[prod_b[1].__name__]:
                    result1 = prod_b[1](int(prod_u[1](int(plate_num[1]))), int(prod_u[2](int(plate_num[2]))))
                    if result1 == None:
                        continue
                    result2 = prod_b[0](int(prod_u[0](int(plate_num[0]))), result1)
                    if result2 == None:
                        continue
                else:
                    result1 =prod_b[0](int(prod_u[0](int(plate_num[0]))), int(prod_u[1](int(plate_num[1]))))
                    if result1 == None:
                        continue
                    result2 = prod_b[1](result1, int(prod_u[2](int(plate_num[2]))))
                    if result2 == None:
                        continue
                    
                if result2 == int(plate_num[3]):
                    total_num += 1
                    solution = Equation(
                        int(plate_num[0]),
                        prod_u[0],
                        prod_b[0],
                        int(plate_num[1]),
                        prod_u[1],
                        prod_b[1],
                        int(plate_num[2]),
                        prod_u[2],
                        int(plate_num[3]),
                        0
                    )
        
        # Adding to the list
        solution_list.append({
            "plate_num": plate_num[:-1] + "-" + plate_num[-1],
            "solution": solution,
            "total_num": total_num
        })          

# 5. Writing to the .csv file
csv_file = 'registration.csv'
def record_statistics():
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['plate_num', 'solution', 'total_num'])

        for item in solution_list:
            writer.writerow([item['plate_num'], item['solution'], item['total_num']])

    print(f"The data is recorded in '{csv_file}'.")

perform_operations()
record_statistics()

# 6. BONUS: if a solution is found immediately move to the next plate
bonus_solution_list = []
def perform_bonus_operations():

    # for each license plate...
    for plate_num in all_registrations:
        can_be_solved = False

        # for each combination of unary operations...
        product_unary_operations =  itertools.product(unary_operations, repeat=3)
        for prod_u in product_unary_operations:

            if can_be_solved:
                break

            # for each combination of binary operations...
            product_binary_operations =  itertools.product(binary_operations, repeat=2)
            for prod_b in product_binary_operations:

                # CASE 1: when the parenthesis is in the first place
                result1 = prod_b[0](int(prod_u[0](int(plate_num[0]))), int(prod_u[1](int(plate_num[1]))))
                if result1 == None:
                    continue
                result2 = prod_b[1](result1, int(prod_u[2](int(plate_num[2]))))
                if result2 == None:
                    continue
                else:
                    if result2 == int(plate_num[3]):
                        can_be_solved = True
                        break

                # CASE 2: when the parenthesis is in the second place
                result1 = prod_b[1](int(prod_u[1](int(plate_num[1]))), int(prod_u[2](int(plate_num[2]))))
                if result1 == None:
                    continue
                result2 = prod_b[0](int(prod_u[0](int(plate_num[0]))), result1)
                if result2 == None:
                    continue
                else:
                    if result2 == int(plate_num[3]):
                        can_be_solved = True
                        break

                # CASE 3: when there are no parentheses, priority is considered
                if operator_precedence[prod_b[0].__name__] < operator_precedence[prod_b[1].__name__]:
                    result1 = prod_b[1](int(prod_u[1](int(plate_num[1]))), int(prod_u[2](int(plate_num[2]))))
                    if result1 == None:
                        continue
                    result2 = prod_b[0](int(prod_u[0](int(plate_num[0]))), result1)
                    if result2 == None:
                        continue
                else:
                    result1 =prod_b[0](int(prod_u[0](int(plate_num[0]))), int(prod_u[1](int(plate_num[1]))))
                    if result1 == None:
                        continue
                    result2 = prod_b[1](result1, int(prod_u[2](int(plate_num[2]))))
                    if result2 == None:
                        continue
                    
                if result2 == int(plate_num[3]):
                    can_be_solved = True
                    break

        # Adding to the list
        bonus_solution_list.append({
            "plate_num": plate_num[:-1] + "-" + plate_num[-1],
            "can_be_solved": can_be_solved
        })

bonus_csv_file = 'registration_bonus.csv'
def record_bonus_statistics():
    with open(bonus_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['plate_num', 'can_be_solved'])

        for item in bonus_solution_list:
            writer.writerow([item['plate_num'], item['can_be_solved']])

    print(f"The data is recorded in '{bonus_csv_file}'.")

perform_bonus_operations()
record_bonus_statistics()