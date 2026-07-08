import random
import time


# ----------------------------------------------------------
# Partition function used by Quickselect
# ----------------------------------------------------------
def partition(arr, low, high, pivot_index):
    pivot = arr[pivot_index]

    # Move pivot to end
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]

    store_index = low

    for i in range(low, high):
        if arr[i] < pivot:
            arr[i], arr[store_index] = arr[store_index], arr[i]
            store_index += 1

    arr[store_index], arr[high] = arr[high], arr[store_index]

    return store_index


# ----------------------------------------------------------
# Randomized Quickselect
# Expected Time: O(n)
# ----------------------------------------------------------
def randomized_quickselect(arr, low, high, k):

    if low == high:
        return arr[low]

    pivot_index = random.randint(low, high)

    pivot_index = partition(arr, low, high, pivot_index)

    if k == pivot_index:
        return arr[k]

    elif k < pivot_index:
        return randomized_quickselect(arr, low, pivot_index - 1, k)

    else:
        return randomized_quickselect(arr, pivot_index + 1, high, k)


# ----------------------------------------------------------
# Median of Medians Algorithm
# Worst Case Time: O(n)
# ----------------------------------------------------------
def median_of_medians(arr, k):

    if len(arr) <= 5:
        return sorted(arr)[k]

    groups = []

    for i in range(0, len(arr), 5):
        group = sorted(arr[i:i + 5])
        groups.append(group[len(group) // 2])

    pivot = median_of_medians(groups, len(groups) // 2)

    lows = []
    highs = []
    pivots = []

    for value in arr:
        if value < pivot:
            lows.append(value)
        elif value > pivot:
            highs.append(value)
        else:
            pivots.append(value)

    if k < len(lows):
        return median_of_medians(lows, k)

    elif k < len(lows) + len(pivots):
        return pivot

    else:
        return median_of_medians(
            highs,
            k - len(lows) - len(pivots)
        )


# ----------------------------------------------------------
# Performance Test
# ----------------------------------------------------------
def run_test(size):

    data = random.sample(range(size * 10), size)

    k = len(data) // 2

    random_copy = data.copy()

    start = time.perf_counter()

    randomized_quickselect(
        random_copy,
        0,
        len(random_copy) - 1,
        k
    )

    random_time = time.perf_counter() - start

    deterministic_copy = data.copy()

    start = time.perf_counter()

    median_of_medians(
        deterministic_copy,
        k
    )

    deterministic_time = time.perf_counter() - start

    print("Size:", size)
    print("Randomized:", random_time)
    print("Deterministic:", deterministic_time)
    print()


sizes = [1000, 5000, 10000]

for size in sizes:
    run_test(size)