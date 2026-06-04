# Partition using the first element as pivot
def deterministic_partition(arr, low, high):

    # Select the first element as pivot
    pivot = arr[low]

    # Initialize left and right pointers
    left = low + 1
    right = high

    while True:

        # Move left pointer while elements are <= pivot
        while left <= right and arr[left] <= pivot:
            left += 1

        # Move right pointer while elements are >= pivot
        while left <= right and arr[right] >= pivot:
            right -= 1

        # Stop if pointers cross
        if left > right:
            break

        # Swap misplaced elements
        arr[left], arr[right] = arr[right], arr[left]

    # Place pivot in its final position
    arr[low], arr[right] = arr[right], arr[low]

    # Return pivot index
    return right


# Recursive Deterministic Quicksort
def deterministic_quicksort(arr, low, high):

    # Continue only if subarray has more than one element
    if low < high:

        # Partition the array
        pivot = deterministic_partition(arr, low, high)

        # Sort left subarray
        deterministic_quicksort(arr, low, pivot - 1)

        # Sort right subarray
        deterministic_quicksort(arr, pivot + 1, high)


# Example usage
arr = [8, 4, 2, 9, 5, 1, 7]

print("Original Array:", arr)

deterministic_quicksort(arr, 0, len(arr) - 1)

print("Sorted Array:", arr)