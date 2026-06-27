import random
import time

# Partition function using the last element as the pivot
def partition(arr, low, high):

    # Choose the last element as the pivot
    pivot = arr[high]

    # Index of the smaller element
    i = low - 1

    # Rearrange elements around the pivot
    for j in range(low, high):

        # Move elements smaller than or equal to the pivot
        if arr[j] <= pivot:
            i += 1

            # Swap elements
            arr[i], arr[j] = arr[j], arr[i]

    # Place the pivot in its correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1


# Deterministic Quicksort
def quicksort(arr, low, high):

    # Continue if more than one element exists
    if low < high:

        # Partition the array
        pivot = partition(arr, low, high)

        # Sort left subarray
        quicksort(arr, low, pivot - 1)

        # Sort right subarray
        quicksort(arr, pivot + 1, high)