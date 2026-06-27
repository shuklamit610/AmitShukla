# Measure execution time
def measure_time(sort_function, arr):

    # Copy the original array
    data = arr.copy()

    # Record start time
    start = time.perf_counter()

    # Execute sorting algorithm
    sort_function(data, 0, len(data) - 1)

    # Record end time
    end = time.perf_counter()

    return end - start


# Different input sizes
sizes = [1000, 5000, 10000]

for size in sizes:

    print(f"\nInput Size: {size}")

    # Random array
    random_array = [random.randint(1, 100000) for _ in range(size)]

    # Sorted array
    sorted_array = sorted(random_array)

    # Reverse sorted array
    reverse_array = sorted(random_array, reverse=True)

    print("Random Input")
    print("Deterministic:", measure_time(quicksort, random_array))
    print("Randomized   :", measure_time(randomized_quicksort, random_array))

    print("\nSorted Input")
    print("Deterministic:", measure_time(quicksort, sorted_array))
    print("Randomized   :", measure_time(randomized_quicksort, sorted_array))

    print("\nReverse Sorted Input")
    print("Deterministic:", measure_time(quicksort, reverse_array))
    print("Randomized   :", measure_time(randomized_quicksort, reverse_array))