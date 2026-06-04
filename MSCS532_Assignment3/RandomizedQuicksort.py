import random

# Select a random pivot and partition the array
def randomized_partition(arr, low, high):

    # Choose a random index between low and high
    pivot_index = random.randint(low, high)

    # Move the random pivot to the end of the array
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]

    # Use the last element as the pivot
    pivot = arr[high]

    # Index of the smaller element
    i = low - 1

    # Rearrange elements around the pivot
    for j in range(low, high):

        # If current element is less than or equal to pivot
        if arr[j] <= pivot:
            i += 1

            # Swap elements
            arr[i], arr[j] = arr[j], arr[i]

    # Place pivot in its correct sorted position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    # Return pivot position
    return i + 1


# Recursive Randomized Quicksort function
def randomized_quicksort(arr, low, high):

    # Continue only if there is more than one element
    if low < high:

        # Partition the array and get pivot index
        pivot = randomized_partition(arr, low, high)

        # Sort left subarray
        randomized_quicksort(arr, low, pivot - 1)

        # Sort right subarray
        randomized_quicksort(arr, pivot + 1, high)


# Wrapper function for sorting
def sort_array(arr):

    # Return immediately if array has 0 or 1 element
    if len(arr) <= 1:
        return arr

    # Sort the entire array
    randomized_quicksort(arr, 0, len(arr) - 1)

    return arr


# Example usage
arr = [8, 4, 2, 9, 5, 1, 7]

print("Original Array:", arr)

sorted_arr = sort_array(arr)

print("Sorted Array:", sorted_arr)