def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    sorted_list = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1

    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])

    return sorted_list

    
if __name__ == "__main__": # pragma: no cover
    sample_array = [38, 27, 43, 3, 9, 82, 10]
    sample_two = [5, 2, 9, 1, 5]
    # print("Original array:", sample_array)
    sorted_array = merge_sort(sample_array)
    # sorted_array_2 = merge_sort(sample_two)
    print("Sorted array:", sorted_array)
    # print("sorted array:", sorted_array_2)