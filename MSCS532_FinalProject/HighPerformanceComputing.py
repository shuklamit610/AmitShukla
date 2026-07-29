# Import Python's built-in time module.
# The time module allows us to measure how long
# each matrix multiplication operation takes.
import time

# Import NumPy for optimized numerical array operations.
# NumPy stores numerical data efficiently and provides
# optimized functions for mathematical calculations.
import numpy as np


# ---------------------------------------------------------
# Function: matrix_multiply_python
# Purpose:
#     Multiplies two matrices using standard Python lists
#     and three nested loops.
#
# This represents the less optimized implementation.
# ---------------------------------------------------------
def matrix_multiply_python(A, B):

    # Get the number of rows in matrix A.
    rows_A = len(A)

    # Get the number of columns in matrix A.
    # This is also the number of rows in matrix B
    # required for matrix multiplication.
    cols_A = len(A[0])

    # Get the number of columns in matrix B.
    cols_B = len(B[0])

    # Create an empty result matrix.
    # Every value is initially set to zero.
    result = [
        [0 for _ in range(cols_B)]
        for _ in range(rows_A)
    ]

    # Loop through each row of matrix A.
    for i in range(rows_A):

        # Loop through each column of matrix B.
        for j in range(cols_B):

            # Store the calculated value for
            # the current position in the result.
            total = 0

            # Multiply corresponding values from
            # matrix A and matrix B.
            for k in range(cols_A):

                # Add the product of the two values
                # to the running total.
                total += A[i][k] * B[k][j]

            # Store the final calculated value
            # in the result matrix.
            result[i][j] = total

    # Return the completed matrix.
    return result


# ---------------------------------------------------------
# Function: create_python_matrix
# Purpose:
#     Creates a square matrix using standard Python lists.
# ---------------------------------------------------------
def create_python_matrix(size):

    # Create a two-dimensional Python list.
    # The values are generated using a simple pattern
    # so that the matrix contains numerical data.
    return [
        [float((i + j) % 10) for j in range(size)]
        for i in range(size)
    ]


# ---------------------------------------------------------
# Function: test_python_matrix
# Purpose:
#     Measures the execution time of matrix multiplication
#     using standard Python lists.
# ---------------------------------------------------------
def test_python_matrix(size):

    # Create the first input matrix.
    A = create_python_matrix(size)

    # Create the second input matrix.
    B = create_python_matrix(size)

    # Record the starting time before multiplication.
    start_time = time.perf_counter()

    # Perform matrix multiplication using
    # the standard Python implementation.
    matrix_multiply_python(A, B)

    # Record the ending time after multiplication.
    end_time = time.perf_counter()

    # Calculate and return the total execution time.
    return end_time - start_time


# ---------------------------------------------------------
# Function: test_numpy_matrix
# Purpose:
#     Measures the execution time of matrix multiplication
#     using NumPy arrays and optimized operations.
# ---------------------------------------------------------
def test_numpy_matrix(size):

    # Create a random NumPy matrix.
    # NumPy stores the numerical values in an efficient
    # array structure designed for numerical computation.
    A = np.random.rand(size, size)

    # Create the second random NumPy matrix.
    B = np.random.rand(size, size)

    # Record the starting time before multiplication.
    start_time = time.perf_counter()

    # Perform matrix multiplication using NumPy.
    # The operation is implemented using optimized
    # low-level numerical routines.
    np.matmul(A, B)

    # Record the ending time after multiplication.
    end_time = time.perf_counter()

    # Calculate and return the total execution time.
    return end_time - start_time


# ---------------------------------------------------------
# Main Performance Experiment
# ---------------------------------------------------------

# Define the matrix sizes that will be tested.
# Larger matrices require more computation.
sizes = [50, 100, 200, 300]

# Display the title of the experiment.
print("HPC Data Structure Optimization Experiment")

# Print a separator to make the output easier to read.
print("-" * 50)


# Run the experiment for each matrix size.
for size in sizes:

    # Measure the execution time of the
    # standard Python list implementation.
    python_time = test_python_matrix(size)

    # Measure the execution time of the
    # optimized NumPy implementation.
    numpy_time = test_numpy_matrix(size)

    # Display the matrix size being tested.
    print(f"Matrix Size: {size} x {size}")

    # Display the execution time for Python lists.
    print(f"Python Lists: {python_time:.6f} seconds")

    # Display the execution time for NumPy arrays.
    print(f"NumPy Arrays: {numpy_time:.6f} seconds")

    # Make sure the NumPy execution time is greater than zero
    # before calculating the speedup.
    if numpy_time > 0:

        # Calculate how many times faster the NumPy
        # implementation is compared with Python lists.
        speedup = python_time / numpy_time

        # Display the calculated speedup.
        print(f"Speedup: {speedup:.2f}x")

    # Print a separator between each test.
    print("-" * 50)