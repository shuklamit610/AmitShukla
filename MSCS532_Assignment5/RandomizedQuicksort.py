# Randomized partition
def randomized_partition(arr, low, high):

    # Select a random pivot
    random_index = random.randint(low, high)

    # Swap random pivot with last element
    arr[random_index], arr[high] = arr[high], arr[random_index]

    # Perform normal partition
    return partition(arr, low, high)


# Randomized Quicksort
def randomized_quicksort(arr, low, high):

    # Continue if more than one element exists
    if low < high:

        # Partition using a random pivot
        pivot = randomized_partition(arr, low, high)

        # Sort left side
        randomized_quicksort(arr, low, pivot - 1)

        # Sort right side
        randomized_quicksort(arr, pivot + 1, high)