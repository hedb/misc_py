
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify


# Generic function to compute partial sums using a loop
def compute_partial_sum(C, a_n, b_n, step_number):
    # Start with the last denominator
    result = b_n[step_number - 1]

    # Loop backwards from step_number - 1 down to 1
    for i in range(step_number - 1, 0, -1):
        result = b_n[i - 1] + a_n[i - 1] / result

    # Apply the constant C to the final result
    return C / result


# Testing function to ensure correctness
def test_generic_partial_sums():
    C = -4
    a_n = [1, 4, 9, 16]
    b_n = [-1, -3, -5, -7]

    # Expected results
    expected_sums = [4.0, 3.0, 3.166666666666667, 3.1372549019607847]

    # Compute and compare
    for i in range(1, 5):
        result = compute_partial_sum(C, a_n, b_n, i)
        assert abs(result - expected_sums[i - 1]) < 1e-9, f"Test failed at step {i}: {result} != {expected_sums[i - 1]}"
        print(f"Test passed for step {i}: {result} == {expected_sums[i - 1]}")

# Function to compute fraction results based on the formula
def generate_fraction_results(fraction_params, steps=10):
    x_values = list(range(1, steps + 1))
    y_values = []

    constant, numerator_formula, denominator_formula = fraction_params
    n = symbols('n')

    # Use sympify to parse formulas
    numerator_expr = sympify(numerator_formula)
    denominator_expr = sympify(denominator_formula)
    numerator_fn = lambdify(n, numerator_expr)
    denominator_fn = lambdify(n, denominator_expr)

    a_n = [numerator_fn(i) for i in x_values]
    b_n = [denominator_fn(i) for i in x_values]

    # Calculate partial sums using the compute_partial_sum function
    for step in range(1, steps + 1):
        result = compute_partial_sum(constant, a_n[:step], b_n[:step], step)
        y_values.append(result)

    return x_values, y_values

# Function to plot the continued fraction results
def plot_fractions(fractions_list):
    plt.figure(figsize=(10, 6))

    # Iterate over each fraction definition in the input list
    for idx, fraction_params in enumerate(fractions_list):
        x_values, y_values = generate_fraction_results(fraction_params)

        # Plotting the results with an ID label
        plt.plot(x_values, y_values, label=f'Fraction {idx + 1}')

    # Add title and labels
    plt.title('Continued Fraction Convergence')
    plt.xlabel('Steps')
    plt.ylabel('Fraction Result')

    # Build legend with formulas and IDs
    legend_labels = [f'Fraction {idx + 1}: a_n={fraction[1]}, b_n={fraction[2]}'
                     for idx, fraction in enumerate(fractions_list)]
    plt.legend(legend_labels)

    # Show the plot
    plt.grid(True)
    plt.show()

# Test input: list of fractions [constant, "numerator formula", "denominator formula"]
fractions_input = [
    [-4, "n**2", "1 - 2*n"],
    [-4, "-2*n**2 + 3*n", "2 - 3*n"],
    [-4, "(n+1)**2", "2 + 2*n"],  # Adjusted to avoid division by zero
    [-4, "-(n**2 - n)", "3 - 4*n"],
    [-4, "-n**2 + 4*n", "1 + n"],  # Adjusted to avoid division by zero
    [-4, "-n**3 + 5*n**2", "1 - 3*n"],
    [-4, "log(n+1)", "2 + 2*n"]   # Adjusted to avoid division by zero
]

# Plot the fractions
plot_fractions(fractions_input)

# https://chatgpt.com/c/67004bc3-e4c4-8008-8786-e18e714461b4
