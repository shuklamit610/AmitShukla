# Insertion Sort in Monotonically Decreasing Order
# Based on the algorithm presented in Chapter 2 of
# "Introduction to Algorithms" by Cormen et al.

def insertion_sort_desc(arr):
    """
    Sorts a list in monotonically decreasing order using Insertion Sort.
    """

    # Start from the second element
    for j in range(1, len(arr)):
        key = arr[j]
        i = j - 1

        # Shift smaller elements to the right
        while i >= 0 and arr[i] < key:
            arr[i + 1] = arr[i]
            i -= 1

        # Insert the key at the correct position
        arr[i + 1] = key

    return arr


# Take input from the user
user_input = input("Enter numbers separated by spaces: ")

# Convert the input string into a list of integers
numbers = list(map(int, user_input.split()))

# Display the original array
print("Original array:", numbers)

# Sort the array in decreasing order
sorted_numbers = insertion_sort_desc(numbers)

# Display the sorted array
print("Sorted array in decreasing order:", sorted_numbers)