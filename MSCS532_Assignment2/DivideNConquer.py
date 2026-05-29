# Import required libraries
import random
import time
import tracemalloc


# -----------------------------------
# QUICK SORT FUNCTION
# -----------------------------------

def quick_sort(arr):

    # Base case:
    # If array has 0 or 1 element, it is already sorted
    if len(arr) <= 1:
        return arr

    # Choose the middle element as pivot
    pivot = arr[len(arr) // 2]

    # Create list of elements smaller than pivot
    left = [x for x in arr if x < pivot]

    # Create list of elements equal to pivot
    middle = [x for x in arr if x == pivot]

    # Create list of elements greater than pivot
    right = [x for x in arr if x > pivot]

    # Recursively sort left and right parts
    return quick_sort(left) + middle + quick_sort(right)


# -----------------------------------
# MERGE SORT FUNCTION
# -----------------------------------

def merge_sort(arr):

    # Base case:
    # If array has 0 or 1 element, it is already sorted
    if len(arr) <= 1:
        return arr

    # Find middle index
    mid = len(arr) // 2

    # Divide array into two halves
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    # Merge sorted halves
    return merge(left, right)


# -----------------------------------
# MERGE FUNCTION
# -----------------------------------

def merge(left, right):

    # Create empty list to store merged result
    result = []

    # Initialize pointers
    i = 0
    j = 0

    # Compare elements from both lists
    while i < len(left) and j < len(right):

        # Add smaller element to result
        if left[i] < right[j]:
            result.append(left[i])
            i += 1

        else:
            result.append(right[j])
            j += 1

    # Add remaining elements from left list
    result.extend(left[i:])

    # Add remaining elements from right list
    result.extend(right[j:])

    return result


# -----------------------------------
# PERFORMANCE TEST FUNCTION
# -----------------------------------

def test_algorithm(name, algorithm, data):

    # Start tracking memory usage
    tracemalloc.start()

    # Record start time
    start_time = time.perf_counter()

    # Run sorting algorithm
    algorithm(data.copy())

    # Record end time
    end_time = time.perf_counter()

    # Get current and peak memory usage
    current, peak = tracemalloc.get_traced_memory()

    # Stop memory tracking
    tracemalloc.stop()

    # Calculate execution time
    execution_time = end_time - start_time

    # Display results
    print(f"{name}")
    print(f"Execution Time: {execution_time:.6f} seconds")
    print(f"Peak Memory Usage: {peak / 1024:.2f} KB")
    print("-" * 40)


# -----------------------------------
# CREATE DATASETS
# -----------------------------------

# Size of dataset
SIZE = 10000

# Create sorted dataset
sorted_data = list(range(SIZE))

# Create reverse sorted dataset
reverse_sorted_data = list(range(SIZE, 0, -1))

# Create random dataset
random_data = random.sample(range(SIZE), SIZE)


# -----------------------------------
# RUN PERFORMANCE TESTS
# -----------------------------------

print("\n===== SORTED DATA =====\n")

# Test Quick Sort on sorted data
test_algorithm("Quick Sort", quick_sort, sorted_data)

# Test Merge Sort on sorted data
test_algorithm("Merge Sort", merge_sort, sorted_data)


print("\n===== REVERSE SORTED DATA =====\n")

# Test Quick Sort on reverse sorted data
test_algorithm("Quick Sort", quick_sort, reverse_sorted_data)

# Test Merge Sort on reverse sorted data
test_algorithm("Merge Sort", merge_sort, reverse_sorted_data)


print("\n===== RANDOM DATA =====\n")

# Test Quick Sort on random data
test_algorithm("Quick Sort", quick_sort, random_data)

# Test Merge Sort on random data
test_algorithm("Merge Sort", merge_sort, random_data)