import random
import time
import heapq

# Heapsort
def heapsort(arr):
    heap = arr[:]
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(len(heap))]

# Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

# Quicksort
def quicksort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quicksort(left) + middle + quicksort(right)

# Benchmark
sizes = [1000, 5000, 10000]

for size in sizes:
    data = [random.randint(1, 100000) for _ in range(size)]

    start = time.time()
    heapsort(data.copy())
    heap_time = time.time() - start

    start = time.time()
    merge_sort(data.copy())
    merge_time = time.time() - start

    start = time.time()
    quicksort(data.copy())
    quick_time = time.time() - start

    print(f"\nSize: {size}")
    print(f"Heapsort: {heap_time:.6f}")
    print(f"Merge Sort: {merge_time:.6f}")
    print(f"Quicksort: {quick_time:.6f}")