import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, lambdify, sympify

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

    print(f"Calculating series for: Constant={constant}, a_n={numerator_formula}, b_n={denominator_formula}")

    for step in range(1, steps + 1):
        result = 0  # Start with 0 for each step
        for i in range(step, 0, -1):
            numerator = numerator_fn(i)
            denominator = denominator_fn(i) + result
            result = numerator / denominator  # Update result

        # Multiply the constant if needed
        final_result = constant * result
        y_values.append(final_result)
        print(f"Step {step}: Result = {final_result}")

    return x_values, y_values



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
    # [-4, "-2*n**2 + 3*n", "-1 - 3*n"],
    [-4, "n**2", "-1*(2*n-1)"]
]

# Plot the fractions
plot_fractions(fractions_input)
