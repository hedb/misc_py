import csv
from datetime import datetime

import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify
import numpy as np
import pandas as pd


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
        # print(f"Test passed for step {i}: {result} == {expected_sums[i - 1]}")

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
    plt.show(block=False)

def plot_samples():
    fractions_input = [
        [-4, "n**2", "1 - 2*n"],
        [-4, "-2*n**2 + 3*n", "2 - 3*n"]
    ]

    plot_fractions(fractions_input)



# Function to compute a_n and b_n based on the parameters
def generate_a_n_b_n(a, b, c, d, f, steps=10):
    n_values = np.arange(1, steps + 1)
    a_n = a * n_values**2 + b * n_values + c
    b_n = d * n_values + f
    return a_n, b_n


def iterate_range_and_output(param_range, file_, C):
    with open(file_, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['running_id', 'a', 'b', 'c', 'd', 'f', 'result'])

        running_id = 0
        target_for_printing = 2
        start = datetime.now()
        # Iterate over all combinations of a, b, c, d, f
        for a in param_range:
            for b in param_range:
                for c in param_range:
                    for d in param_range:
                        for f in param_range:
                            running_id += 1
                            try:
                                # Generate a_n and b_n for the given parameters
                                a_n, b_n = generate_a_n_b_n(a, b, c, d, f)
                                # Compute the result for the continued fraction after 10 steps
                                result = compute_partial_sum(C, a_n, b_n, 10)
                                # Write the result to the CSV file
                                writer.writerow([running_id, a, b, c, d, f, result])
                            except ZeroDivisionError:
                                # Skip combinations that result in division by zero
                                continue
                            if (running_id == target_for_printing):
                                target_for_printing *= 2
                                print(f"Running ID: {running_id}, time_elapsed: {datetime.now() - start}")


    print(f"Results written to {file_}")

def generate_range_csv():
    # Example usage of the function
    param_range = np.arange(-5, 5, 0.5)
    output_file = 'continued_fractions_results.csv'
    C = -4
    iterate_range_and_output(param_range, output_file, C)


def hist(filename):
    # Load the data from the CSV file
    data = pd.read_csv(filename)
    # data = pd.read_csv('test.csv')

    # Extract the 'result' column
    results = data['result']

    # Plot a histogram of the results
    plt.figure(figsize=(10, 6))
    plt.hist(results, bins=100, color='blue', edgecolor='black')

    # Add labels and title
    plt.title('Distribution of Continued Fraction Results', fontsize=16)
    plt.xlabel('Result', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)

    # Show the plot
    plt.grid(True)
    plt.show(block=False)


def bounded_hist(min_, max_):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv('cleaned_continued_fractions_results.csv')
    # df = pd.read_csv('test.csv')

    # Filter the DataFrame for 'result' values between min_ and max_
    filtered_df = df[(df['result'] >= min_) & (df['result'] <= max_)]
    # print the len
    print(len(filtered_df))

    # Create the histogram
    plt.hist(filtered_df['result'], bins=10, edgecolor='black')
    plt.title(f'Histogram of Results Between {min_} and {max_}')
    plt.xlabel('Result')
    plt.ylabel('Frequency')
    plt.show(block=False)




def clean_data():
    # Load the data from the CSV file
    data = pd.read_csv('continued_fractions_results.csv')

    # Remove rows where the 'result' column is 'inf'
    cleaned_data = data.replace([np.inf, -np.inf], np.nan).dropna(subset=['result'])

    # Save the cleaned data to a new CSV file (optional)
    cleaned_data.to_csv('cleaned_continued_fractions_results.csv', index=False)


def extract_and_deep_dive(x, y, steps, output_file):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv('cleaned_continued_fractions_results.csv')

    # Filter the DataFrame for 'result' values between x and y
    filtered_df = df[(df['result'] >= x) & (df['result'] <= y)]

    # Open the output file for writing
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['running_id', 'a', 'b', 'c', 'd', 'f', 'result'])

        # Iterate over the filtered DataFrame rows
        for index, row in filtered_df.iterrows():
            a, b, c, d, f = row['a'], row['b'], row['c'], row['d'], row['f']

            # Generate a_n and b_n using the existing function
            a_n, b_n = generate_a_n_b_n(a, b, c, d, f, steps=steps)

            # Recalculate the result using the compute_partial_sum function
            recalculated_result = compute_partial_sum(C=-4, a_n=a_n, b_n=b_n, step_number=steps)

            # Write the recalculated result along with parameters to the output file
            writer.writerow([row['running_id'], a, b, c, d, f, recalculated_result])

    print(f"Recalculated results saved to {output_file}")


# https://chatgpt.com/c/67004bc3-e4c4-8008-8786-e18e714461b4
if __name__ == "__main__":
    test_generic_partial_sums()
    # plot_samples()
    # generate_range_csv()
    # clean_data()
    # hist()
    bounded_hist(3.1, 3.2)
    extract_and_deep_dive( 3.1, 3.2, 10, 'recalculated_results.csv')
    hist('recalculated_results.csv')

    plt.pause(100)