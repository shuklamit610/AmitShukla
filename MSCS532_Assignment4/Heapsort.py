# Heapsort Implementation using a Max Heap

def heapify(arr, n, i):
    """
    Maintains the max-heap property for a subtree rooted at index i.
    """

    largest = i
    left = (2 * i) + 1
    right = (2 * i) + 2

    # Check if left child is larger than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Check if right child is larger than current largest
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If largest is not root, swap and continue heapifying
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heapsort(arr):
    """
    Sorts an array using the Heapsort algorithm.
    """
    n = len(arr)

    # Build max heap
    for i in range((n // 2) - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        # Move current root to end
        arr[i], arr[0] = arr[0], arr[i]

        # Heapify reduced heap
        heapify(arr, i, 0)

    return arr


# Example usage
data = [12, 11, 13, 5, 6, 7]
print("Sorted Array:", heapsort(data))