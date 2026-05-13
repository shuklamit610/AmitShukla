# Insertion Sort in Monotonically Decreasing Order
# Based on the algorithm presented in Chapter 2 of
# "Introduction to Algorithms" by Cormen et al.

def insertion_sort_desc(arr):
    """
    Sorts a list in monotonically decreasing order using Insertion Sort.
    
    Parameters:
        arr (list): List of numbers to be sorted.
    
    Returns:
        list: Sorted list in decreasing order.
    """
    
    # Traverse through elements starting from the second element
    for j in range(1, len(arr)):
        key = arr[j]      # Element to be inserted into the sorted portion
        i = j - 1

        # Move elements that are smaller than 'key'
        # one position ahead to make room for 'key'
        while i >= 0 and arr[i] < key:
            arr[i + 1] = arr[i]
            i = i - 1

        # Insert the key in its correct position
        arr[i + 1] = key

    return arr


# Example usage
numbers = [5, 2, 4, 6, 1, 3]

print("Original array:", numbers)

sorted_numbers = insertion_sort_desc(numbers)

print("Sorted array in decreasing order:", sorted_numbers)